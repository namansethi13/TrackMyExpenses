"""
Utility script to create an ngrok tunnel and set up Telegram webhook for localhost development.
"""

import os
import subprocess
import time
import requests
from typing import Optional

from chat_interfaces.telegram import TelegramInterface, ChatInterfaceError
from core.logger import get_logger

logger = get_logger(__name__)


class LocalhostWebhookManager:
    """Manages ngrok tunnel creation and Telegram webhook setup for local development."""
    
    def __init__(self, local_port: int = 8000):
        """
        Initialize the webhook manager.
        
        Args:
            local_port (int): The local port where FastAPI is running (default: 8000)
        """
        self.local_port = local_port
        self.tunnel_process = None
        self.public_url = None
    
    def create_ngrok_tunnel(self, proto: str = "http") -> Optional[str]:
        """
        Create an ngrok tunnel to expose localhost to the internet.
        
        Args:
            proto (str): The protocol to use (default: "http")
        
        Returns:
            Optional[str]: The public ngrok URL if successful, None otherwise
        """
        try:
            # Check if ngrok is installed
            result = subprocess.run(
                ["ngrok", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                logger.error("ngrok is not installed. Please install it first.")
                logger.info("Visit https://ngrok.com to download and install ngrok.")
                return None
            
            logger.info(f"Starting ngrok tunnel on port {self.local_port}...")
            
            # Start ngrok in the background
            self.tunnel_process = subprocess.Popen(
                ["ngrok", proto, str(self.local_port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give ngrok time to start and establish the tunnel
            time.sleep(3)
            
            # Query ngrok API to get the public URL
            try:
                api_response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
                api_response.raise_for_status()
                
                tunnels = api_response.json().get("tunnels", [])
                if tunnels:
                    # Get the first tunnel's public URL
                    public_url = tunnels[0].get("public_url")
                    if public_url:
                        self.public_url = public_url
                        logger.info(f"Ngrok tunnel created: {public_url}")
                        return public_url
            except Exception as e:
                logger.error(f"Error querying ngrok API: {e}")
                if self.tunnel_process:
                    self.tunnel_process.terminate()
                return None
            
        except FileNotFoundError:
            logger.error("ngrok executable not found in PATH.")
            logger.info("Please ensure ngrok is installed and added to your system PATH.")
        except Exception as e:
            logger.error(f"Error creating ngrok tunnel: {e}")
        
        return None
    
    def setup_telegram_webhook(
        self,
        telegram_bot_token: str,
        webhook_url: Optional[str] = None
    ) -> bool:
        """
        Set up Telegram webhook for development using ngrok tunnel.
        
        Args:
            telegram_bot_token (str): Your Telegram bot token
            webhook_url (Optional[str]): Custom webhook URL. If None, creates ngrok tunnel
        
        Returns:
            bool: True if webhook was set successfully, False otherwise
        """
        try:
            # Create ngrok tunnel if no webhook URL provided
            if webhook_url is None:
                webhook_url = self.create_ngrok_tunnel()
                if webhook_url is None:
                    logger.error("Failed to create ngrok tunnel. Cannot proceed with webhook setup.")
                    return False
            
            # Initialize Telegram interface and set webhook
            telegram_interface = TelegramInterface()
            
            # Append webhook path if not already included
            if not webhook_url.endswith("/webhook/telegram"):
                webhook_url = f"{webhook_url}/webhook/telegram"
            
            telegram_interface.setWebhook(
                bot_token=telegram_bot_token,
                webhook_url=webhook_url
            )
            
            logger.info(f"Telegram webhook successfully set to: {webhook_url}")
            return True
                
        except ChatInterfaceError as e:
            logger.error(f"Failed to set Telegram webhook: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error setting up Telegram webhook: {e}")
            return False
    
    def cleanup(self) -> None:
        """Clean up tunnel process."""
        if self.tunnel_process:
            try:
                self.tunnel_process.terminate()
                logger.info("Ngrok tunnel terminated.")
            except Exception as e:
                logger.error(f"Error terminating tunnel: {e}")


if __name__ == "__main__":
    import sys
    
    # Get bot token from environment or command line
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        if len(sys.argv) > 1:
            bot_token = sys.argv[1]
        else:
            logger.error("Telegram bot token not provided.")
            logger.info("Usage: python localhost_webhook_to_tg.py <bot_token>")
            logger.info("Or set TELEGRAM_BOT_TOKEN environment variable.")
            sys.exit(1)
    
    local_port = int(os.getenv("LOCAL_PORT", "8000"))
    
    # Initialize manager and set up webhook
    manager = LocalhostWebhookManager(local_port)
    success = manager.setup_telegram_webhook(bot_token)
    
    if success:
        # Keep the script running
        try:
            logger.info("Press Ctrl+C to stop the tunnel")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            manager.cleanup()
    else:
        sys.exit(1)
