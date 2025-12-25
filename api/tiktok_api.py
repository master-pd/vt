# -*- coding: utf-8 -*-
"""
TIKTOK API WRAPPER
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import re
import time
import json
import random
from typing import Dict, List, Optional, Tuple
from utils.logger import Logger
from utils.validator import Validator

class TikTokAPI:
    def __init__(self):
        self.logger = Logger("tiktok_api")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        self.session = None
        self.proxies = {}
        
    def initialize_session(self):
        """Initialize HTTP session"""
        import requests
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def set_proxy(self, proxy_config: Dict):
        """Set proxy for requests"""
        if proxy_config and 'proxy' in proxy_config:
            proxy_url = proxy_config['proxy']
            proxy_type = proxy_config.get('type', 'http')
            
            self.proxies = {
                'http': f'{proxy_type}://{proxy_url}',
                'https': f'{proxy_type}://{proxy_url}'
            }
            self.logger.info(f"Proxy set: {proxy_url}")
        else:
            self.proxies = {}
            
    def extract_video_info(self, url: str) -> Dict:
        """Extract video information from URL"""
        try:
            # Validate URL
            is_valid, message = Validator.validate_tiktok_url(url)
            if not is_valid:
                return {'error': message}
            
            # Extract video ID
            video_id = Validator.extract_video_id(url)
            if not video_id:
                return {'error': 'Could not extract video ID'}
            
            # Get video page
            response = self._make_request(url)
            if not response:
                return {'error': 'Failed to fetch video page'}
            
            # Parse video data
            video_data = self._parse_video_data(response.text, video_id)
            
            return {
                'success': True,
                'video_id': video_id,
                'url': url,
                'data': video_data
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting video info: {e}")
            return {'error': str(e)}
    
    def get_video_views(self, url: str) -> Optional[int]:
        """Get current view count for a video"""
        try:
            info = self.extract_video_info(url)
            if 'error' in info:
                return None
            
            # Try to get views from parsed data
            data = info.get('data', {})
            views = data.get('viewCount', 0)
            
            if views > 0:
                return views
            
            # Alternative method: make API request
            video_id = info['video_id']
            api_url = f"https://www.tiktok.com/api/v1/video/detail/?video_id={video_id}"
            
            response = self._make_request(api_url)
            if response and response.status_code == 200:
                api_data = response.json()
                if 'itemInfo' in api_data:
                    views = api_data['itemInfo'].get('itemStruct', {}).get('stats', {}).get('playCount', 0)
                    return views
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting video views: {e}")
            return None
    
    def simulate_view(self, url: str, account_data: Dict = None, proxy_config: Dict = None) -> bool:
        """Simulate a view on a video"""
        try:
            if proxy_config:
                self.set_proxy(proxy_config)
            
            # Extract video ID
            video_id = Validator.extract_video_id(url)
            if not video_id:
                self.logger.error(f"Could not extract video ID from {url}")
                return False
            
            # Step 1: Visit video page
            video_response = self._make_request(url)
            if not video_response:
                self.logger.error("Failed to load video page")
                return False
            
            # Step 2: Extract required tokens/headers
            tokens = self._extract_tokens(video_response.text)
            
            # Step 3: Simulate watch time
            watch_time = random.randint(3000, 15000)  # 3-15 seconds
            time.sleep(watch_time / 1000)
            
            # Step 4: Optional: Like the video
            if account_data and random.random() > 0.7:  # 30% chance to like
                self._simulate_like(video_id, tokens, account_data)
            
            # Step 5: Optional: Follow user
            if account_data and random.random() > 0.9:  # 10% chance to follow
                self._simulate_follow(video_id, tokens, account_data)
            
            self.logger.debug(f"View simulated for video {video_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error simulating view: {e}")
            return False
    
    def _make_request(self, url: str, method: str = 'GET', data: Dict = None, retry: int = 3):
        """Make HTTP request with retry logic"""
        if not self.session:
            self.initialize_session()
        
        for attempt in range(retry):
            try:
                if method == 'GET':
                    response = self.session.get(url, proxies=self.proxies, timeout=30)
                elif method == 'POST':
                    response = self.session.post(url, json=data, proxies=self.proxies, timeout=30)
                else:
                    return None
                
                if response.status_code == 200:
                    return response
                
                self.logger.warning(f"Request failed with status {response.status_code}, attempt {attempt + 1}")
                
                # Add delay before retry
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                self.logger.warning(f"Request error: {e}, attempt {attempt + 1}")
                time.sleep(2 ** attempt)
        
        return None
    
    def _parse_video_data(self, html_content: str, video_id: str) -> Dict:
        """Parse video data from HTML"""
        data = {
            'video_id': video_id,
            'viewCount': 0,
            'likeCount': 0,
            'commentCount': 0,
            'shareCount': 0,
            'author': {},
            'music': {},
            'hashtags': []
        }
        
        try:
            # Try to find JSON-LD data
            import json
            json_ld_pattern = r'<script type="application/ld\+json">(.*?)</script>'
            matches = re.findall(json_ld_pattern, html_content, re.DOTALL)
            
            for match in matches:
                try:
                    json_data = json.loads(match.strip())
                    if '@type' in json_data and json_data['@type'] == 'VideoObject':
                        if 'interactionCount' in json_data:
                            data['viewCount'] = int(json_data['interactionCount'])
                        if 'author' in json_data:
                            data['author'] = json_data['author']
                        break
                except:
                    continue
            
            # Try to find TikTok's internal data
            tiktok_pattern = r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'
            tiktok_match = re.search(tiktok_pattern, html_content, re.DOTALL)
            
            if tiktok_match:
                try:
                    tiktok_data = json.loads(tiktok_match.group(1).strip())
                    
                    # Navigate to video data
                    video_info = tiktok_data.get('__DEFAULT_SCOPE__', {}).get('webapp.video-detail', {}).get('itemInfo', {}).get('itemStruct', {})
                    
                    if video_info:
                        stats = video_info.get('stats', {})
                        data['viewCount'] = stats.get('playCount', data['viewCount'])
                        data['likeCount'] = stats.get('diggCount', 0)
                        data['commentCount'] = stats.get('commentCount', 0)
                        data['shareCount'] = stats.get('shareCount', 0)
                        
                        author = video_info.get('author', {})
                        data['author'] = {
                            'id': author.get('id'),
                            'username': author.get('uniqueId'),
                            'nickname': author.get('nickname')
                        }
                        
                        music = video_info.get('music', {})
                        data['music'] = {
                            'id': music.get('id'),
                            'title': music.get('title'),
                            'author': music.get('authorName')
                        }
                        
                        # Extract hashtags
                        text = video_info.get('desc', '')
                        hashtags = re.findall(r'#(\w+)', text)
                        data['hashtags'] = hashtags
                        
                except Exception as e:
                    self.logger.debug(f"Error parsing TikTok data: {e}")
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error parsing video data: {e}")
            return data
    
    def _extract_tokens(self, html_content: str) -> Dict:
        """Extract CSRF tokens and other required tokens from HTML"""
        tokens = {
            'csrf_token': '',
            'session_id': '',
            'device_id': ''
        }
        
        try:
            # Extract CSRF token
            csrf_pattern = r'<meta name="csrf-token" content="(.*?)">'
            csrf_match = re.search(csrf_pattern, html_content)
            if csrf_match:
                tokens['csrf_token'] = csrf_match.group(1)
            
            # Extract session ID from cookies
            if self.session:
                cookies = self.session.cookies.get_dict()
                if 'sessionid' in cookies:
                    tokens['session_id'] = cookies['sessionid']
                if 'tt_webid' in cookies:
                    tokens['device_id'] = cookies['tt_webid']
            
            return tokens
            
        except Exception as e:
            self.logger.debug(f"Error extracting tokens: {e}")
            return tokens
    
    def _simulate_like(self, video_id: str, tokens: Dict, account_data: Dict):
        """Simulate liking a video"""
        try:
            like_url = f"https://www.tiktok.com/api/comment/like/"
            
            headers = {
                'X-CSRFToken': tokens.get('csrf_token', ''),
                'X-Session-ID': tokens.get('session_id', ''),
                'Content-Type': 'application/json'
            }
            
            data = {
                'item_id': video_id,
                'type': 1,  # 1 for like
                'count': 1
            }
            
            # Add account-specific headers if available
            if 'cookie' in account_data:
                headers['Cookie'] = account_data['cookie']
            
            response = self._make_request(like_url, method='POST', data=data)
            
            if response and response.status_code == 200:
                self.logger.debug(f"Like simulated for video {video_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Error simulating like: {e}")
            return False
    
    def _simulate_follow(self, video_id: str, tokens: Dict, account_data: Dict):
        """Simulate following a user"""
        try:
            # First get author ID from video
            video_url = f"https://www.tiktok.com/api/v1/video/detail/?video_id={video_id}"
            response = self._make_request(video_url)
            
            if not response or response.status_code != 200:
                return False
            
            video_data = response.json()
            author_id = video_data.get('itemInfo', {}).get('itemStruct', {}).get('author', {}).get('id')
            
            if not author_id:
                return False
            
            # Send follow request
            follow_url = "https://www.tiktok.com/api/user/follow/"
            
            headers = {
                'X-CSRFToken': tokens.get('csrf_token', ''),
                'X-Session-ID': tokens.get('session_id', ''),
                'Content-Type': 'application/json'
            }
            
            data = {
                'user_id': author_id,
                'type': 1  # 1 for follow
            }
            
            # Add account-specific headers if available
            if 'cookie' in account_data:
                headers['Cookie'] = account_data['cookie']
            
            response = self._make_request(follow_url, method='POST', data=data)
            
            if response and response.status_code == 200:
                self.logger.debug(f"Follow simulated for user {author_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Error simulating follow: {e}")
            return False
    
    def check_account_status(self, username: str, password: str) -> Dict:
        """Check TikTok account status"""
        try:
            # This would require actual TikTok login
            # For simulation, return random status
            
            statuses = ['active', 'active', 'active', 'limited', 'banned']
            weights = [0.7, 0.7, 0.7, 0.2, 0.1]  # Higher chance for active
            
            status = random.choices(statuses, weights=weights, k=1)[0]
            
            return {
                'username': username,
                'status': status,
                'last_checked': time.time(),
                'views_available': random.randint(100, 1000) if status == 'active' else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error checking account status: {e}")
            return {'error': str(e)}
    
    def validate_proxy(self, proxy_config: Dict) -> Tuple[bool, Dict]:
        """Validate proxy by making test request to TikTok"""
        try:
            old_proxies = self.proxies
            self.set_proxy(proxy_config)
            
            test_url = "https://www.tiktok.com/@tiktok"
            response = self._make_request(test_url, retry=1)
            
            self.proxies = old_proxies
            
            if response and response.status_code == 200:
                speed = response.elapsed.total_seconds() * 1000  # Convert to ms
                
                # Check if TikTok page loaded (basic check)
                if 'tiktok' in response.text.lower():
                    return True, {
                        'status': 'working',
                        'speed_ms': round(speed, 2),
                        'country': self._detect_proxy_country(response.text)
                    }
            
            return False, {'status': 'failed', 'error': 'Request failed'}
            
        except Exception as e:
            return False, {'status': 'error', 'error': str(e)}
    
    def _detect_proxy_country(self, html_content: str) -> str:
        """Detect proxy country from response"""
        # Try to detect country from HTML
        country_patterns = {
            'US': ['america', 'united states', 'usa'],
            'GB': ['united kingdom', 'britain', 'uk'],
            'DE': ['germany', 'deutschland'],
            'FR': ['france', 'french'],
            'JP': ['japan', 'japanese'],
            # Add more patterns as needed
        }
        
        html_lower = html_content.lower()
        
        for country_code, patterns in country_patterns.items():
            for pattern in patterns:
                if pattern in html_lower:
                    return country_code
        
        return 'Unknown'