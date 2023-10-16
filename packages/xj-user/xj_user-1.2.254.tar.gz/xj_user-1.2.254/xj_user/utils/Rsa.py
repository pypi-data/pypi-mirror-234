from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
import base64


def encrypt_password(pwd, dypub_pem, salt):
    # 将动态公钥从PEM格式加载为RSA公钥对象
    dypub = load_pem_public_key(dypub_pem.encode())

    # 生成密钥派生函数（KDF）的参数
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
    )

    # 使用KDF和密码生成加密密钥
    key = kdf.derive(pwd.encode())

    # 使用动态公钥加密密钥
    encrypted_key = dypub.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 将加密密钥编码为Base64，以便于传输
    cip = base64.b64encode(encrypted_key).decode()

    return cip


# 示例用法
# pwd = "user_password"
# dypub_pem = """
# -----BEGIN PUBLIC KEY-----
# ... your public key in PEM format ...
# -----END PUBLIC KEY-----
# """
# salt = "a1b2c3"
#
# cip = encrypt_password(pwd, dypub_pem, salt)
# print("传输密文 (cip):", cip)


def decrypt_password(cip, privkey_pem, salt, passphrase=None):
    # 将私钥从PEM格式加载为RSA私钥对象
    privkey = load_pem_private_key(privkey_pem.encode(), password=passphrase, backend=None)

    # 解码Base64编码的密文，以获取加密密钥
    encrypted_key = base64.b64decode(cip)

    # 使用私钥解密密钥
    key = privkey.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 生成密钥派生函数（KDF）的参数
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
    )

    # 验证解密后的密钥与原始密码是否匹配
    try:
        kdf.verify(key, key)
        print("密码匹配")
    except Exception:
        print("密码不匹配")


# 示例用法
# cip = "your_base64_encoded_encrypted_key"
# privkey_pem = """
# -----BEGIN PRIVATE KEY-----
# ... your private key in PEM format ...
# -----END PRIVATE KEY-----
# """
# salt = "a1b2c3"
# passphrase = None  # 如果您的私钥有密码，请提供
#
# decrypt_password(cip, privkey_pem, salt, passphrase)
