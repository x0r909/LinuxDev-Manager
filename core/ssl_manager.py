"""SSL certificate manager."""
import os
from typing import Tuple
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtensionOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import datetime
from utils.system_utils import run_command, write_file
from core.config_manager import ConfigManager


class SSLManager:
    """Manages SSL certificates."""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize SSL manager.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config = config_manager
    
    def generate_self_signed_certificate(
        self,
        domain: str,
        days_valid: int = 365
    ) -> Tuple[bool, str]:
        """
        Generate a self-signed SSL certificate.
        
        Args:
            domain: Domain name
            days_valid: Number of days the certificate is valid
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            
            # Generate certificate
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "LinuxDev Manager"),
                x509.NameAttribute(NameOID.COMMON_NAME, domain),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.datetime.utcnow()
            ).not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=days_valid)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName(domain),
                    x509.DNSName(f"www.{domain}"),
                ]),
                critical=False,
            ).sign(private_key, hashes.SHA256(), default_backend())
            
            # Serialize private key
            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            # Serialize certificate
            cert_pem = cert.public_bytes(serialization.Encoding.PEM)
            
            # Save certificate and key
            cert_path = f"/etc/ssl/certs/{domain}.crt"
            key_path = f"/etc/ssl/private/{domain}.key"
            
            # Write certificate
            if not write_file(cert_path, cert_pem.decode('utf-8'), use_sudo=True):
                return False, "Failed to write certificate file"
            
            # Write private key
            if not write_file(key_path, private_key_pem.decode('utf-8'), use_sudo=True):
                return False, "Failed to write private key file"
            
            # Set permissions
            run_command(f'chmod 644 {cert_path}', use_sudo=True)
            run_command(f'chmod 600 {key_path}', use_sudo=True)
            
            return True, f"SSL certificate generated successfully for {domain}"
        
        except Exception as e:
            return False, f"Failed to generate certificate: {str(e)}"
    
    def install_certificate(self, domain: str) -> Tuple[bool, str]:
        """
        Install certificate to system trust store.
        
        Args:
            domain: Domain name
            
        Returns:
            Tuple of (success, message)
        """
        cert_path = f"/etc/ssl/certs/{domain}.crt"
        
        if not os.path.exists(cert_path):
            return False, f"Certificate not found: {cert_path}"
        
        try:
            # Copy to ca-certificates
            returncode, _, stderr = run_command(
                f'cp {cert_path} /usr/local/share/ca-certificates/{domain}.crt',
                use_sudo=True
            )
            
            if returncode != 0:
                return False, f"Failed to copy certificate: {stderr}"
            
            # Update certificates
            returncode, _, stderr = run_command(
                'update-ca-certificates',
                use_sudo=True
            )
            
            if returncode != 0:
                return False, f"Failed to update certificates: {stderr}"
            
            return True, f"Certificate installed for {domain}"
        
        except Exception as e:
            return False, f"Failed to install certificate: {str(e)}"
    
    def remove_certificate(self, domain: str) -> Tuple[bool, str]:
        """
        Remove SSL certificate.
        
        Args:
            domain: Domain name
            
        Returns:
            Tuple of (success, message)
        """
        cert_path = f"/etc/ssl/certs/{domain}.crt"
        key_path = f"/etc/ssl/private/{domain}.key"
        ca_cert_path = f"/usr/local/share/ca-certificates/{domain}.crt"
        
        # Remove files
        run_command(f'rm -f {cert_path}', use_sudo=True)
        run_command(f'rm -f {key_path}', use_sudo=True)
        run_command(f'rm -f {ca_cert_path}', use_sudo=True)
        
        # Update certificates
        run_command('update-ca-certificates', use_sudo=True)
        
        return True, f"Certificate removed for {domain}"
    
    def certificate_exists(self, domain: str) -> bool:
        """
        Check if certificate exists for domain.
        
        Args:
            domain: Domain name
            
        Returns:
            True if certificate exists
        """
        cert_path = f"/etc/ssl/certs/{domain}.crt"
        key_path = f"/etc/ssl/private/{domain}.key"
        
        return os.path.exists(cert_path) and os.path.exists(key_path)
