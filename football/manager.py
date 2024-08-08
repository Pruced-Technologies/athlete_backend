from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password = None, password2=None, **extra_fields):
        
        # if not extra_fields['email']:
        #     raise ValueError("Email is required")

        if not email:
            raise ValueError("Email is required")
        
        if not extra_fields['username']:
            raise ValueError("Username is required")
        
        # if not extra_fields['username']:
        #     raise ValueError("Username is required")
        
        # extra_fields['email'] = self.normalize_email(extra_fields['email'])
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user
    
    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_verified',True)
        extra_fields.setdefault('is_subscribed',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff to True')
        
        return self.create_user(email, password, password2=None, **extra_fields)