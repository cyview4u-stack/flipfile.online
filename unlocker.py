import asyncio
from pathlib import Path
import logging
from typing import Optional, List, Dict, Any
import itertools

logger = logging.getLogger(__name__)

class PDFUnlocker:
    """Unlock/remove password protection from PDF files"""
    
    def __init__(self):
        self.common_passwords = [
            "password", "123456", "12345678", "1234", "12345",
            "qwerty", "abc123", "password1", "admin", "welcome",
            "letmein", "monkey", "dragon", "sunshine", "iloveyou",
            "trustno1", "123123", "football", "baseball", "superman"
        ]
        
        # Dictionary attack wordlist (basic)
        self.wordlist = self.common_passwords + [
            "secret", "private", "protected", "secure", "confidential",
            "document", "file", "pdf", "user", "owner", "2023", "2024",
            "company", "business", "personal", "work", "home", "office"
        ]
    
    async def unlock(self, input_path: Path, password: Optional[str] = None) -> Path:
        """Unlock PDF file"""
        
        output_dir = Path("processed")
        output_path = output_dir / f"unlocked_{input_path.name}"
        
        # First, check if PDF is encrypted
        if not await self._is_encrypted(input_path):
            # Not encrypted, just copy
            import shutil
            shutil.copy2(input_path, output_path)
            return output_path
        
        # Try provided password first
        if password:
            try:
                return await self._unlock_with_password(input_path, output_path, password)
            except Exception as e:
                logger.info(f"Provided password failed: {e}")
        
        # Try common passwords
        logger.info("Trying common passwords...")
        for common_pass in self.common_passwords:
            try:
                return await self._unlock_with_password(input_path, output_path, common_pass)
            except:
                continue
        
        # Try dictionary attack
        logger.info("Trying dictionary attack...")
        unlocked = await self._dictionary_attack(input_path, output_path)
        if unlocked:
            return unlocked
        
        # Try brute force on simple patterns
        logger.info("Trying brute force on simple patterns...")
        unlocked = await self._brute_force_simple(input_path, output_path)
        if unlocked:
            return unlocked
        
        # If all else fails, try to remove encryption without password
        # (this will only work with certain types of encryption)
        try:
            return await self._remove_encryption(input_path, output_path)
        except Exception as e:
            logger.error(f"All unlock methods failed: {e}")
            raise Exception("Unable to unlock PDF. Please provide correct password.")
    
    async def _is_encrypted(self, input_path: Path) -> bool:
        """Check if PDF is encrypted"""
        try:
            import pikepdf
            
            with pikepdf.open(input_path) as pdf:
                return pdf.is_encrypted
                
        except pikepdf.PasswordError:
            return True
        except Exception:
            return False
    
    async def _unlock_with_password(self, input_path: Path, output_path: Path, 
                                   password: str) -> Path:
        """Unlock PDF with specific password"""
        try:
            import pikepdf
            
            # Try to open with password
            pdf = pikepdf.open(input_path, password=password)
            
            # Save without encryption
            pdf.save(output_path, encryption=False)
            pdf.close()
            
            logger.info(f"Successfully unlocked with password: {password}")
            return output_path
            
        except pikepdf.PasswordError:
            raise Exception("Incorrect password")
        except Exception as e:
            raise Exception(f"Unlock error: {str(e)}")
    
    async def _dictionary_attack(self, input_path: Path, output_path: Path, 
                                max_attempts: int = 1000) -> Optional[Path]:
        """Try dictionary attack with wordlist"""
        try:
            import pikepdf
            
            attempts = 0
            for word in self.wordlist:
                if attempts >= max_attempts:
                    break
                
                # Try word as-is
                try:
                    pdf = pikepdf.open(input_path, password=word)
                    pdf.save(output_path, encryption=False)
                    pdf.close()
                    logger.info(f"Dictionary attack successful: {word}")
                    return output_path
                except pikepdf.PasswordError:
                    attempts += 1
                
                # Try with common variations
                variations = [
                    word.upper(),
                    word.capitalize(),
                    word + "123",
                    "123" + word,
                    word + "!",
                    word + "?"
                ]
                
                for variation in variations:
                    if attempts >= max_attempts:
                        break
                    
                    try:
                        pdf = pikepdf.open(input_path, password=variation)
                        pdf.save(output_path, encryption=False)
                        pdf.close()
                        logger.info(f"Dictionary attack successful: {variation}")
                        return output_path
                    except pikepdf.PasswordError:
                        attempts += 1
            
            return None
            
        except Exception as e:
            logger.error(f"Dictionary attack error: {e}")
            return None
    
    async def _brute_force_simple(self, input_path: Path, output_path: Path,
                                 max_length: int = 4) -> Optional[Path]:
        """Brute force attack for simple passwords"""
        try:
            import pikepdf
            
            # Character sets
            digits = "0123456789"
            lowercase = "abcdefghijklmnopqrstuvwxyz"
            uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            # Try all digit combinations up to max_length
            for length in range(1, max_length + 1):
                for combo in itertools.product(digits, repeat=length):
                    password = ''.join(combo)
                    
                    try:
                        pdf = pikepdf.open(input_path, password=password)
                        pdf.save(output_path, encryption=False)
                        pdf.close()
                        logger.info(f"Brute force successful: {password}")
                        return output_path
                    except pikepdf.PasswordError:
                        continue
            
            return None
            
        except Exception as e:
            logger.error(f"Brute force error: {e}")
            return None
    
    async def _remove_encryption(self, input_path: Path, output_path: Path) -> Path:
        """Attempt to remove encryption without password"""
        try:
            # This method tries to repair corrupted encryption metadata
            import pikepdf
            
            # Try to open with empty password
            try:
                pdf = pikepdf.open(input_path, password="")
                pdf.save(output_path, encryption=False)
                pdf.close()
                return output_path
            except:
                pass
            
            # Try with QPDF repair
            try:
                pdf = pikepdf.open(input_path, allow_overwriting_input=True)
                
                # Remove encryption info from trailer
                if '/Encrypt' in pdf.trailer:
                    del pdf.trailer['/Encrypt']
                
                # Clear encryption from all objects
                for obj in pdf.objects.values():
                    if hasattr(obj, '/Encrypt'):
                        del obj['/Encrypt']
                
                pdf.save(output_path, encryption=False)
                pdf.close()
                return output_path
                
            except Exception as e:
                raise Exception(f"Encryption removal failed: {e}")
                
        except Exception as e:
            logger.error(f"Remove encryption error: {e}")
            raise
    
    async def batch_unlock(self, input_paths: List[Path], 
                          password: Optional[str] = None) -> List[Path]:
        """Unlock multiple PDF files"""
        tasks = []
        for input_path in input_paths:
            task = self.unlock(input_path, password)
            tasks.append(task)
        
        return await asyncio.gather(*tasks)
    
    async def get_encryption_info(self, input_path: Path) -> Dict[str, Any]:
        """Get information about PDF encryption"""
        try:
            import pikepdf
            
            info = {
                "is_encrypted": False,
                "encryption_type": None,
                "permissions": {},
                "metadata_encrypted": False,
                "version": None
            }
            
            try:
                pdf = pikepdf.open(input_path)
                info["is_encrypted"] = pdf.is_encrypted
                
                if pdf.is_encrypted:
                    # Try to get encryption details
                    try:
                        # Get encryption dictionary
                        if '/Encrypt' in pdf.trailer:
                            encrypt = pdf.trailer['/Encrypt']
                            info["encryption_type"] = str(encrypt.get('/Filter', ''))
                            info["version"] = str(encrypt.get('/V', ''))
                            info["length"] = str(encrypt.get('/Length', ''))
                    except:
                        pass
                
                pdf.close()
                
            except pikepdf.PasswordError:
                info["is_encrypted"] = True
                info["requires_password"] = True
            
            return info
            
        except Exception as e:
            logger.error(f"Encryption info error: {e}")
            return {"is_encrypted": False, "error": str(e)}
    
    async def estimate_unlock_time(self, input_path: Path, 
                                  method: str = "dictionary") -> Dict[str, Any]:
        """Estimate time required to unlock"""
        info = await self.get_encryption_info(input_path)
        
        if not info["is_encrypted"]:
            return {"estimated_time": "0 seconds", "method": "none"}
        
        estimates = {
            "dictionary": "1-5 minutes",
            "brute_force_simple": "5-30 minutes",
            "brute_force_complex": "hours to days",
            "impossible": "Not possible without password"
        }
        
        # Check encryption strength
        encryption_type = info.get("encryption_type", "")
        if "AES" in encryption_type or info.get("length") == "256":
            return {
                "estimated_time": estimates["impossible"],
                "method": "password_required",
                "strength": "strong"
            }
        
        return {
            "estimated_time": estimates.get(method, "unknown"),
            "method": method,
            "strength": "weak" if "RC4" in encryption_type else "moderate"
        }
