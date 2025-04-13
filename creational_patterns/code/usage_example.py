from human_models import Seller, Buyer, Admin

# factory method usage
admin = Admin(name='<ADMIN_NAME>', email='<ADMIN_EMAIL>')
seller = Seller(name='<Seller_NAME>', email='<Seller_EMAIL>')
buyer = Buyer(name='<Buyer_NAME>', email='<Buyer_EMAIL>')
objects = [admin, seller, buyer]

for obj in objects:
    obj.register()
    obj.login()
    obj.logout()
