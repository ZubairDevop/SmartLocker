
# SmartLocker seed.py

# Importing Flask application and database
from app import create_app, db

# werkzeug.security will hash user passwords before storing in database
from werkzeug.security import generate_password_hash

# Importing application database models
from app.models.user import User
from app.models.laptop_model import LaptopModel
from app.models.locker import Locker
from app.models.locker_cell import LockerCell
from app.models.request import Request

#Importing application all constants such as roles, statuses and categories
from app.constants import *

app = create_app()

# Seed data for users
# Contains admin and standard users across multiple departments
users_data = [
("Zubair","Ahmad","zubaira","IT","IT Support Engineer",CATEGORY_STANDARD,ROLE_ADMIN),
("Uzair","Ahmad","uzaira","IT","IT Support Engineer",CATEGORY_STANDARD,ROLE_ADMIN),
("Clare","Daldry","clared","IT","IT Support Manager",CATEGORY_STANDARD,ROLE_ADMIN),
("Brian","Cooke","brianc","IT","IT Support Engineer",CATEGORY_STANDARD,ROLE_ADMIN),
("Tracey","Beaumont","traceyb","IT","IT Support Engineer",CATEGORY_STANDARD,ROLE_ADMIN),
("Clark","Kent","clarkk","IT","IT Support Engineer",CATEGORY_STANDARD,ROLE_ADMIN),

("Tony","Stark","tonys","Finance","Director",CATEGORY_EXECUTIVE,ROLE_USER),
("Steve","Rogers","stever","Customer Service","Customer Service Advisor",CATEGORY_STANDARD,ROLE_USER),
("Bruce","Banner","bruceb","R&D","Scientist",CATEGORY_STANDARD,ROLE_USER),
("Natasha","Romanoff","natashar","Security","Security Manager",CATEGORY_STANDARD,ROLE_USER),
("Nick","Fury","nickf","IT","Head of Department",CATEGORY_EXECUTIVE,ROLE_USER),
("Diana","Prince","dianap","HR","Head of Department",CATEGORY_EXECUTIVE,ROLE_USER),
("Peter","Parker","peterp","Customer Service","Customer Service Advisor",CATEGORY_STANDARD,ROLE_USER),
("Bruce","Wayne","brucew","Finance","Director",CATEGORY_EXECUTIVE,ROLE_USER),
("Barry","Allen","barrya","Finance","Finance Assistant",CATEGORY_STANDARD,ROLE_USER),
("Hal","Jordan","halj","Sales","Sales Executive",CATEGORY_STANDARD,ROLE_USER),
("Arthur","Curry","arthurc","Procurement","Procurement Officer",CATEGORY_STANDARD,ROLE_USER),
("Victor","Stone","victors","IT","IT Support Engineer",CATEGORY_STANDARD,ROLE_USER),
("Oliver","Queen","oliverq","Sales","Director",CATEGORY_EXECUTIVE,ROLE_USER),
("Lois","Lane","loisl","Marketing","Marketing Executive",CATEGORY_STANDARD,ROLE_USER),
("Selina","Kyle","selinak","Legal","Legal Assistant",CATEGORY_STANDARD,ROLE_USER),
("Barbara","Gordon","barbarag","HR","HR Administrator",CATEGORY_STANDARD,ROLE_USER),
("Dick","Grayson","dickg","IT","Service Desk Analyst",CATEGORY_STANDARD,ROLE_USER),
("Kate","Kane","katek","Finance","Finance Assistant",CATEGORY_STANDARD,ROLE_USER),
("John","Stewart","johns","IT","Infrastructure Engineer",CATEGORY_STANDARD,ROLE_USER),
("Billy","Batson","billyb","Sales","Sales Executive",CATEGORY_STANDARD,ROLE_USER),
("Kara","Danvers","karad","Marketing","Marketing Executive",CATEGORY_STANDARD,ROLE_USER),
("Logan","Howlett","loganh","IT","IT Support Engineer",CATEGORY_STANDARD,ROLE_USER),
("Jean","Grey","jeang","HR","HR Administrator",CATEGORY_STANDARD,ROLE_USER),
("Charles","Xavier","charlesx","HR","Director",CATEGORY_EXECUTIVE,ROLE_USER),
("Scott","Lang","scottl","Customer Service","Customer Service Advisor",CATEGORY_STANDARD,ROLE_USER),
("Wanda","Maximoff","wandam","Finance","Finance Assistant",CATEGORY_STANDARD,ROLE_USER),
("Vision","Vision","vision","IT","Infrastructure Engineer",CATEGORY_STANDARD,ROLE_USER),
("Sam","Wilson","samw","Sales","Sales Executive",CATEGORY_STANDARD,ROLE_USER),
("Bucky","Barnes","buckyb","IT","Service Desk Analyst",CATEGORY_STANDARD,ROLE_USER),
("Carol","Danvers","carold","Marketing","Marketing Executive",CATEGORY_STANDARD,ROLE_USER),
("Stephen","Strange","stephens","Legal","Director",CATEGORY_EXECUTIVE,ROLE_USER),
("Matt","Murdock","mattm","Legal","Legal Assistant",CATEGORY_STANDARD,ROLE_USER),
("Frank","Castle","frankc","Procurement","Procurement Officer",CATEGORY_STANDARD,ROLE_USER),
("Ororo","Munroe","ororom","HR","HR Administrator",CATEGORY_STANDARD,ROLE_USER),
("Jonn","Jones","jonnj","Customer Service","Head of Department",CATEGORY_EXECUTIVE,ROLE_USER),
("Lex","Luthor","lexl","Finance","Finance Assistant",CATEGORY_STANDARD,ROLE_USER),
("Clint","Barton","clintb","IT","IT Support Engineer",CATEGORY_STANDARD,ROLE_USER),
("Emma","Frost","emmaf","HR","HR Administrator",CATEGORY_STANDARD,ROLE_USER),
]

# seeding data for laptops
laptops_data=[
("Dell","Latitude 5550",CATEGORY_STANDARD),    
("Fujitsu","E5410",CATEGORY_STANDARD),
("Lenovo","L14 Gen 5",CATEGORY_STANDARD),
("Fujitsu","E5513",CATEGORY_STANDARD),
("Dell","Latitude 7450",CATEGORY_STANDARD),
("Lenovo","L13 Gen 4",CATEGORY_STANDARD),
("Dell","Latitude 5450",CATEGORY_STANDARD),
("Microsoft","Surface Pro 11",CATEGORY_EXECUTIVE),
("Apple","MacBook Pro 14",CATEGORY_EXECUTIVE),
("Apple","MacBook Pro 16",CATEGORY_EXECUTIVE),
]

# remove existing table and then create again when seed.py is executed
with app.app_context():
    db.drop_all()
    db.create_all()

# Creating laptop model records
# Each laptop is added to the LaptopModel table
    laptops=[]
    for mfr,model,cat in laptops_data:
        l=LaptopModel(manufacturer=mfr,model=model,category=cat,status=LAPTOP_AVAILABLE)
        db.session.add(l); laptops.append(l)
    db.session.flush()

# this script create user accounts
# Assign a default laptop based on user's category
# Executive users receive an Executive laptop
# Standard users receive a Standard laptop
    users=[]
    std=laptops[0]
    exe=laptops[7]
    for fn,ln,un,dept,title,cat,role in users_data:
        u=User(first_name=fn,last_name=ln,username=un,
               email=f"{un}123@cgi.com",
               department=dept,
               job_title=title,
               assigned_category=cat,
               role=role,
               # Store password securely using hashing
               password_hash=generate_password_hash("Password123!"),
               current_laptop_id=(exe.id if cat==CATEGORY_EXECUTIVE else std.id))
        db.session.add(u); users.append(u)

    db.session.flush()
    
    # Creating a Smart Locker
    locker=Locker(locker_name="Smart Locker")
    db.session.add(locker)
    db.session.flush()

    # 20 cells: 12 std,3 exec,5 empty
    cell=1
    for i in range(12):
        db.session.add(LockerCell(locker_id=locker.id,cell_number=cell,laptop_id=laptops[i%7].id,status=CELL_AVAILABLE)); cell+=1
    for i in range(3):
        db.session.add(LockerCell(locker_id=locker.id,cell_number=cell,laptop_id=laptops[7+i].id,status=CELL_AVAILABLE)); cell+=1
    for i in range(5):
        db.session.add(LockerCell(locker_id=locker.id,cell_number=cell,laptop_id=None,status=CELL_EMPTY)); cell+=1
    db.session.flush()

 # this code Retrieve all locker cells for request allocation
    cells = LockerCell.query.all()

    # populating status in the Request table
    # this will provides a mix of Pending, Ready, Completed, Rejected and Cancelled requests
    statuses = [
        REQUEST_PENDING,
        REQUEST_PENDING,
        REQUEST_READY,
        REQUEST_COMPLETED,
        REQUEST_READY,
        REQUEST_READY,
        REQUEST_COMPLETED,
        REQUEST_COMPLETED,
        REQUEST_REJECTED,
        REQUEST_CANCELLED
    ]

    # both codes are important as it separate users by category to ensure requests match
    # the user's assigned laptop category, so executive can only request exec laptop and standard user can only request standard
    standard_users = [
        user for user in users
        if user.role == ROLE_USER and user.assigned_category == CATEGORY_STANDARD
    ]

    executive_users = [
        user for user in users
        if user.role == ROLE_USER and user.assigned_category == CATEGORY_EXECUTIVE
    ]

# dumpy request data will be populated against these users
    request_users = [
        standard_users[0],
        standard_users[1],
        standard_users[2],
        standard_users[3],
        standard_users[4],
        standard_users[5],
        standard_users[6],
        standard_users[7],
        executive_users[0],
        executive_users[1],
    ]

    # this loop will create replacement requests
    # Each request is linked to a user and assigned a status
    # Rejected requests do not receive a locker allocation
    for i, status in enumerate(statuses):

        selected_user = request_users[i]

        request = Request(
            user_id=selected_user.id,
            requested_category=selected_user.assigned_category,
            locker_cell_id=cells[i].id if status != REQUEST_REJECTED else None,
            issue_description="Laptop damaged and unable to work.",
            priority=PRIORITY_MEDIUM,
            status=status
        )

        db.session.add(request)
 

    db.session.commit()
    print("SmartLocker database seeded successfully.")
