from sqlalchemy import create_engine
from db import *

engine = create_engine('postgresql://postgres@192.168.99.100:5432/kvm')

def main():
    Base.metadata.create_all(engine)
    
if __name__ == '__main__':
    main()
    