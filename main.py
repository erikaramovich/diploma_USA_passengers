# import pandas as pd
import numpy as np
from helper import logger
from dataframe import MyDataFrame
import inquirer
from tabulate import tabulate
from tqdm import tqdm
import time
import os


global DF

try:
    os.mkdir("AnswersResults")
except:
    pass





# 1 FIRST menu to upload the dataset
questions = [
  inquirer.List('action',
                message="Choose action:",
                choices=['Upload dataset', "Upload dot_2016_2019.csv", 'Exit'],
            ),
]
answers = inquirer.prompt(questions)
# 1 END FIRST menu

if answers['action'] == 'Upload dot_2016_2019.csv':
    DF = MyDataFrame("dot_2016_2019.csv")
    DF.make_markets()
        
    for i in tqdm(range(50)):
        time.sleep(0.01)
    print(tabulate(DF.df.head(10), headers='keys', tablefmt='mixed_grid'))
    
elif answers['action'] == 'Upload dataset':
    questions = [
        inquirer.Text('path', message="Enter the path of the file:"),
    ]
    path = inquirer.prompt(questions)["path"]
    
    DF = MyDataFrame(path)
    DF.make_markets()
        
    for i in tqdm(range(50)):
        time.sleep(0.01)
    print(tabulate(DF.df.head(10), headers='keys', tablefmt='mixed_grid'))
else:
    print("Goodbye")
    exit()



while True:
    # 2 SECOND menu for introduction of dataset
    questions = [
    inquirer.List('action',
                    message="Choose action:",
                    choices=['DF.info()', "DF.describe()","DF.uniques()", "Optizimize memory", "Do other operations", 'Exit'],
                ),
    ]
    answers = inquirer.prompt(questions)
    # 2 END SECOND menu

    if answers['action'] == 'DF.info()':
        logger.info("Information about DataFrame")
        print(tabulate(DF.df.info(), headers='keys', tablefmt='mixed_grid'))
    elif answers['action'] == 'DF.describe()':
        logger.info("Description of DataFrame")
        print(tabulate(DF.df.describe(), headers='keys', tablefmt='mixed_grid'))
    elif answers['action'] == 'DF.uniques()':
        logger.info("Unique values of DataFrame")
        pretty_dict = {}
        pretty_dict["column"] = []
        pretty_dict["size"] = []
        pretty_dict["values"] = []
        for column in DF.df.columns:
            unique_values = DF.df[column].unique()
            pretty_dict["column"].append(column)
            pretty_dict["size"].append(len(unique_values))
            pretty_dict["values"].append(unique_values[:4])
        print(tabulate(pretty_dict, headers='keys', tablefmt='mixed_grid'))
        
    elif answers['action'] == 'Optizimize memory':
        logger.info("Optimizing memory")
        for i in tqdm(range(50)):
            time.sleep(0.01)
        DF.df["passengers"] = DF.df["passengers"].astype("int32")
        DF.df["seats"] = DF.df["seats"].astype("int32")
        DF.df["year"] = DF.df["year"].astype("int16")
        DF.df["month"] = DF.df["month"].astype("int8")
        logger.info("Memory optimized")
    elif answers['action'] == 'Do other operations':
        break
    else:
        print("Goodbye")
        exit()




while True:
    # 3 THIRD menu for operations
    questions = [
    inquirer.List('action',
                    message="Choose action:",
                    choices=['Markets', "Extract Cool Markets (Necessary)", "Plot", "Do other operations",'Exit'],
                ),
    ]
    answers = inquirer.prompt(questions)

    if answers['action'] == 'Markets':
        print(tabulate(DF.df.head(10), headers='keys', tablefmt='mixed_grid'))

        # 3.1 MENU for saving markets
        question =inquirer.Confirm("save", message="Save the markets in file?"),
        answer_to_save = inquirer.prompt(question)["save"]
        # 3.1 END MENU for saving markets

        if answer_to_save:
            DF.save_markets()
        else:
            pass
        
    elif answers['action'] == 'Extract Cool Markets (Necessary)':
        DF.make_cool_markets()
        
        # 3.2 MENU for saving cool markets
        question =inquirer.Confirm("save", message="Save the cool markets in file?"),
        answer_to_save = inquirer.prompt(question)["save"]
        # 3.2 END MENU for saving cool markets

        if answer_to_save:
            DF.save_cool_markets()
        else:
            pass

    elif answers['action'] == 'Plot':
        # 3.3 MENU for plotting
        questions = [
            inquirer.List('action',
                            message="Choose action:",
                            choices=["Plot market", 'Random 10 markets', 'Random 10 cool markets'],
                        ),
        ]
        answers = inquirer.prompt(questions)
        # 3.3 END MENU for plotting


        if answers['action'] == 'Plot market':
            
            # 3.3.1 CONFIRM for prefered markets
            question =inquirer.Confirm("plot", message="Do you have prefered market to plot?"),
            answer_to_plot = inquirer.prompt(question)["plot"]
            # 3.3.1 END CONFIRM for prefered markets
            
            if answer_to_plot:
                # 3.3.2 INPUT for prefered market
                questions = [
                    inquirer.Text('market', message="Enter the market name:"),
                ]
                market = inquirer.prompt(questions)["market"]
                # 3.3.2 END INPUT for prefered market

                DF.plot_market(market)
            else:
                DF.plot_market(DF.df_unordered["market"].sample().iloc[0])

        elif answers['action'] == 'Random 10 markets':
            for mark in np.random.choice(DF.list_of_markets, 10):
                print(mark)
            
        elif answers['action'] == 'Random 10 cool markets':
            for mark in np.random.choice(DF.list_of_cool_markets, 10):
                print(mark)
        else:
            pass

    elif answers['action'] == 'Do other operations':
        break
    else:
        print("Goodbye")
        exit()


while True:
    # 4 FOURTH menu for market operations
    questions = [
    inquirer.List('action',
                    message="Choose market size:",
                    choices=['Small', "Medium", "Big", "Do other operations", 'Exit'],
                ),
    ]
    answers = inquirer.prompt(questions)
    # 4 END FOURTH menu for market operations

    if answers['action'] == 'Small':
        DF.make_small_market()
        print(tabulate(DF.df_small.sample(10), headers='keys', tablefmt='mixed_grid'))

        # 4.1 CONFIRM for prefered small market
        question =inquirer.Confirm("prefered", message="Do you have prefered small market to research?"),
        answer_prefered = inquirer.prompt(question)["prefered"]
        # 4.1 END CONFIRM for prefered markets
        
        small_market = None
        if answer_prefered:
            # 4.1.1 INPUT for prefered market
            questions = [
                inquirer.Text('market', message="Enter the small market name:"),
            ]
            small_market = inquirer.prompt(questions)["market"]
            # 4.1.1 END INPUT for prefered market
            if small_market not in DF.df_small["market"].values:
                logger.error(f"Market {small_market} does not exist. Try again")
                continue

            DF.make_heuristic_predection(small_market)
        else:
            DF.make_heuristic_predection(DF.df_small["market"].sample().iloc[0])


    elif answers['action'] == 'Medium':
        DF.make_medium_market()
        print(tabulate(DF.df_medium.sample(10), headers='keys', tablefmt='mixed_grid'))

        # 4.2 CONFIRM for prefered medium market
        question =inquirer.Confirm("prefered", message="Do you have prefered medium market to research?"),
        answer_prefered = inquirer.prompt(question)["prefered"]
        # 4.2 END CONFIRM for prefered markets

        medium_market = None
        if answer_prefered:
            # 4.2.1 INPUT for prefered market
            questions = [
                inquirer.Text('market', message="Enter the medium market name:"),
            ]
            medium_market = inquirer.prompt(questions)["market"]
            # 4.2.1 END INPUT for prefered market

            if medium_market not in DF.df_medium["market"].values:
                logger.error(f"Market {medium_market} does not exist. Try again")
                continue

            DF.make_heuristic_predection(medium_market)
        else:
            DF.make_heuristic_predection(DF.df_medium["market"].sample().iloc[0])


    elif answers['action'] == 'Big':
        DF.make_big_market()
        print(tabulate(DF.df_big.sample(10), headers='keys', tablefmt='mixed_grid'))

        # 4.3 CONFIRM for prefered big market
        question =inquirer.Confirm("prefered", message="Do you have prefered big market to research?"),
        answer_prefered = inquirer.prompt(question)["prefered"]
        # 4.3 END CONFIRM for prefered markets

        big_market = None
        if answer_prefered:
            # 4.3.1 INPUT for prefered market
            questions = [
                inquirer.Text('market', message="Enter the big market name:"),
            ]
            big_market = inquirer.prompt(questions)["market"]
            # 4.3.1 END INPUT for prefered market
            
            if big_market not in DF.df_big["market"].values:
                logger.error(f"Market {big_market} does not exist. Try again")
                continue

            DF.make_heuristic_predection(big_market)
        else:
            DF.make_heuristic_predection(DF.df_big["market"].sample().iloc[0])

    elif answers['action'] == 'Do other operations':
        break
    else:
        print("Goodbye")
        exit()


# while True:
#     # 5 FIFTH menu for saving markets
#     questions = [
#     inquirer.List('action',
#                     message="Choose market size to make heuristic prediction:",
#                     choices=['Small', "Medium", "Big", "Do other operations", 'Exit'],
#                 ),
#     ]
#     answers = inquirer.prompt(questions)
#     # 5 END FIFTH menu for saving markets

#     if answers['action'] == 'Small':
#         pass
#     elif answers['action'] == 'Medium':
#         pass
#     elif answers['action'] == 'Big':
#         pass
#     elif answers['action'] == 'Do other operations':
#         break
#     else:
#         print("Goodbye")
#         exit()

    