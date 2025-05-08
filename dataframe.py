from helper import logger
import inquirer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

class MyDataFrame:
    def __init__(self, path):
        try:
            self.df = pd.read_csv(path)
            logger.info(f"Dataframe was uploaded successfully from the path {path}")
        except Exception as e:
            logger.error(f"error: {e}")
            exit()

    def make_markets(self):
        self.df["market"] = self.df.apply(lambda row: "_".join(sorted([row["origin"], row["destination"]])), axis=1)
        self.df = self.df[(self.df['passengers'] != 0) & (self.df['seats'] != 0)]
        self.df_unordered = self.df.groupby(["market", "year", "month"], as_index=False).agg({"passengers": "sum", "seats": "sum"})
        self.df_unordered["non_zero_passengers"] = self.df_unordered["passengers"] > 0
        logger.info(f"Markets (size:{len(self.df["market"].unique())}) were made successfully")

        # Saving the list of markets
        self.list_of_markets = list(self.df["market"].unique())
    

    def save_markets(self, path="AnswersResults/markets.txt"):
        with open(path, "w") as f:
            f.write("\n".join(self.df["market"].unique()))
        logger.info(f"Markets saved successfully in {path}")


    def make_cool_markets(self):
        market_month_counts = self.df_unordered.groupby("market")["non_zero_passengers"].sum()
        self.cool_markets = market_month_counts[market_month_counts == 48].index.to_list()
        # Saving the list of cool markets
        self.list_of_cool_markets = list(self.cool_markets)
        logger.info(f"Cool markets (size:{len(self.cool_markets)}) extracted successfully")

        self.df_cool = self.df_unordered[self.df_unordered["market"].isin(self.cool_markets)]
        self.df_mean = self.df_cool.groupby('market', as_index=False)['passengers'].mean()
        self.df_mean.rename(columns={'passengers': 'PPM'}, inplace=True)

        min_val = self.df_mean['PPM'].min()
        max_val = self.df_mean['PPM'].max()
        bins = np.logspace(np.log10(min_val), np.log10(max_val), num=20)

        # Plot histogram with logarithmic bins
        plt.hist(self.df_mean['PPM'], bins=bins, edgecolor='black', log=True)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Average Passengers Per Month (PPM)')
        plt.ylabel('Frequency')
        plt.title('Histogram of Average PPM for Cool Markets (Log-Log Scale)')
        
        question = inquirer.Confirm("save", message="Do you want save Average PPM for cool markets plot?"),
        answer_to_save_plot = inquirer.prompt(question)["save"]
        
        if answer_to_save_plot:
            path = f"AnswersResults/AveragePPM_cool_markets.png"
            plt.savefig(path)
            logger.info(f"Average PPM for cool markets plot saved successfully in {path}")
        else:
            pass

        plt.show()



    def save_cool_markets(self, path="AnswersResults/cool_markets.txt"):
        
        with open(path, "w") as f:
            f.write("\n".join(self.cool_markets))
        logger.info(f"Cool Markets saved successfully in {path}")



    def plot_market(self, market):
        if market not in self.df["market"].unique():
            logger.error(f"Market {market} does not exist. Try again")
            return
        
        market_data = self.df_unordered[self.df_unordered["market"] == market]
        market_monthly_passengers = market_data.groupby(["year", "month"])["passengers"].sum()
        market_monthly_passengers.index = pd.to_datetime(market_monthly_passengers.index.map(lambda x: f"{x[0]}-{x[1]}"))
        market_monthly_passengers = market_monthly_passengers.sort_index()

        plt.figure(figsize=(12, 6))
        plt.plot(market_monthly_passengers.index, market_monthly_passengers.values, marker="o", linestyle="-", label="Passengers")
        plt.title(f"Market {market} monthly passengers (2016-2019)")
        plt.xlabel("Time")
        plt.ylabel("Passengers")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        question =inquirer.Confirm("save", message=f"Do you want save {market}'s plot?"),
        answer_to_save_plot = inquirer.prompt(question)["save"]
        
        if answer_to_save_plot:
            path = f"AnswersResults/{market}.png"
            plt.savefig(path)
            logger.info(f"Market {market} plot saved successfully in {path}")
        else:
            pass

        plt.show()        
        logger.info(f"Market {market} plotted successfully")


    def make_small_market(self):
        self.df_small = self.df_mean[self.df_mean["PPM"] < 1000]
        logger.info(f"Small markets (size:{len(self.df_small)}) were made successfully")
        return self.df_small


    def make_medium_market(self):
        self.df_medium = self.df_mean[(self.df_mean["PPM"] >= 1000) & (self.df_mean["PPM"] < 10000)]
        logger.info(f"Medium markets (size:{len(self.df_medium)}) were made successfully")
        return self.df_medium

    def make_big_market(self):
        self.df_big = self.df_mean[self.df_mean["PPM"] >= 10000]
        logger.info(f"Big markets (size:{len(self.df_big)}) were made successfully")
        return self.df_big
    

    @staticmethod
    def predict_linear_heuristic(predict_year :np.array, last_year :np.array) -> np.array:
        y_predict = np.zeros(12)
        for i in range(1, 12):
            y_predict[i] = predict_year[i-1] * (last_year[i] / last_year[i-1])
        
        return y_predict



    def make_heuristic_predection(self, market):
        market_data = self.df[self.df["market"] == market]
        print(tabulate(market_data[:10], headers='keys', tablefmt='mixed_grid'))
        
        self.plot_market(market)

        market_data = self.df_unordered[self.df_unordered["market"] == market]
        market_monthly_passengers = market_data.groupby(["year", "month"])["passengers"].sum()
        market_monthly_passengers = market_monthly_passengers.reset_index()

        while True:
            # MENU about what year user want to predict
            questions = [
                inquirer.List('year',
                                message="Choose year to predict:",
                                choices=[ 2017, 2018, 2019, 'Exit'],
                            ),
            ]
            answers = inquirer.prompt(questions)
            # END MENU about what year user want to predict
            
            if answers['year'] == 'Exit':
                break

            year = answers['year']
            last_year = year - 1

            actual_passengers = market_monthly_passengers[market_monthly_passengers["year"] == year]["passengers"].values
            last_year_passengers = market_monthly_passengers[market_monthly_passengers["year"] == last_year]["passengers"].values

            # Heuristic prediction
            y_pred = self.predict_linear_heuristic(actual_passengers, last_year_passengers)[1:]
            actual_passengers = actual_passengers[1:]

            mape = np.abs(y_pred - actual_passengers) / actual_passengers * 100
            month = ["February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            results = pd.DataFrame({"Month": month, "Real": actual_passengers, "Predicted": y_pred,  "MAPE": mape})
            print(tabulate(results, headers='keys', tablefmt='grid'))
            logger.info(f"Heuristic prediction for market {market} {last_year}-{year} was made successfully")


            predictions = pd.DataFrame({"Month": month, "MAPE": mape})
            predictions["month"] = pd.to_datetime(predictions["Month"], format="%B")
            predictions.plot(x="Month", y="MAPE", kind="line", color="skyblue")
            plt.title(f"MAPE {last_year}-{year} for market {market} prediction")
            plt.savefig(f"AnswersResults/MAPE_{last_year}-{year}_of__{market}.png")
            plt.show()
