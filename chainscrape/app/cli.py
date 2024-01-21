from chainQA import ChainQA
from scraper import Scraper
from utils import create_database,clear_files

def main_menu(): 
    picker = { 
        "S": scrape_menu, 
        "G": gather_menu,
        "Q": qa_menu,
        "C": create_database,
        "DD": clear_files,
        "X": exit
    }
    main_menu_txt = """
    Welcome to Chainscrape. Choose from the following: 

    S)crape a URL for links 
    G)ather text from URLs in the DB
    Q)&A Session
    C)reate DB 
    DD)elete all files
    X)it 

    """
    print(main_menu_txt)
    c = input(i)
    if c in picker:
        picker[c]()

def scrape_menu(): 
    print("Enter url to scrape. Press X to return to main menu.\n")
    c = input(i)
    if c == "X": 
        main_menu()
    else: 
        s = Scraper() 
        try: 
            links = s.scrape_links(c)
            print(links)
            s.store_links(links)
            print("Stored %s links." % len(links))
            main_menu()
        except Exception as e: 
            print(e)
            scrape_menu()

def gather_menu(): 
    print("Gather links from all links in the DB? Type Y to proceed. Type X to return to main menu.")
    c = input(i)
    if c == "X": 
        main_menu()
    elif c == "Y": 
        s = Scraper()
        links = s.query_links()
        counter = 0
        for url in links:
            print("URL is ->", url)
            try: 
                s.store_page_text(url)
            except Exception as e: 
                print(e)
            counter += 1
            if counter == 100:
                main_menu()
        main_menu()
    else: 
        print("Y or X, cowboy.")
        gather_menu()
    

def qa_menu(): 
    cqa = ChainQA()
    cqa.set_llm(temp=1)
    cqa.vectorize() 
    qa = cqa.get_qa_session() 
    print("I am the great and powerful Oz. Ask your question. Type X to return to main menu.")
    c = None
    while c != "X": 
        c = input("> ")
        answer = qa.run(c)
        print(answer)
    main_menu() 

i = "> "
main_menu()


