# # import matplotlib.pyplot as plt

# # months = ["Jan", "Feb", "Mar", "Apr", "May"]
# # sales = [100, 150, 200, 250, 300]

# # plt.plot(months, sales, marker='o', linestyle='-')
# # plt.xlabel("Months")
# # plt.ylabel("Sales ($)")
# # plt.title("Monthly Sales Trend")
# # plt.show()


# import matplotlib.pyplot as plt
# # Data: Sales of different products
# # products = ["Shoes", "Bags", "Watches", "Glasses"]
# # sales = [500, 700, 300, 400]


# # # Create a bar chart
# # plt.bar(products, sales, color='blue')

# # # Labels and title
# # plt.xlabel("Products")  # X-axis label
# # plt.ylabel("Sales ($)")  # Y-axis label
# # plt.title("Product Sales Comparison")  # Chart title

# # plt.show()  # Display the chart


# # import numpy as np  # Import NumPy for random data

# # # Generate random marks for 50 students (0-100)
# # marks = np.random.randint(0, 100, 50)
# # print(marks)

# # # Create a histogram with bins
# # plt.hist(marks, bins=10, color='green', edgecolor='black')

# # # Labels and title
# # plt.xlabel("Marks Range")  # X-axis label
# # plt.ylabel("Number of Students")  # Y-axis label
# # plt.title("Students' Marks Distribution")  # Chart title

# # plt.show()  # Display the chart


# import numpy as np
# import matplotlib.pyplot as plt

# # # Generate random marks for 50 students (0-100)
# # marks = np.random.randint(0, 100, 50)

# # # Separate fail and pass marks
# # fail_marks = [m for m in marks if m < 30]  # Fail (Red)
# # pass_marks = [m for m in marks if m >= 30]  # Pass (Green)

# # # Create a histogram
# # plt.hist(pass_marks, bins=10, color='green', edgecolor='black', label="Pass")
# # plt.hist(fail_marks, bins=5, color='red', edgecolor='black', label="Fail")

# # # # Labels and title
# # # plt.xlabel("Marks Range")
# # # plt.ylabel("Number of Students")
# # # plt.title("Students' Marks Distribution")

# # # # Add legend
# # # plt.legend()

# # # plt.show()  # Display the chart


# # # Data: Heights and Weights
# # heights = [150, 160, 170, 180, 190]
# # weights = [50, 60, 70, 80, 90]

# # # Create a scatter plot
# # plt.scatter(heights, weights, color='red')

# # # Labels and title
# # plt.xlabel("Height (cm)")  # X-axis label
# # plt.ylabel("Weight (kg)")  # Y-axis label
# # plt.title("Height vs Weight")  # Chart title

# # # plt.show()  # Display the chart


# # import matplotlib.pyplot as plt

# # # Example data
# # # advertising_budget = [5, 10, 15, 20, 25, 30, 35, 40, 45]
# # # sales = [7, 9, 14, 18, 20, 23, 25, 28, 30]

# # # # Create scatter plot
# # # plt.figure(figsize=(80, 60))
# # # plt.scatter(advertising_budget, sales, color='blue', edgecolor='black', s=100)

# # # # Add labels and title
# # # plt.title('Advertising Budget vs Sales')
# # # plt.xlabel('Advertising Budget ($1000s)')
# # # plt.ylabel('Sales ($1000s)')

# # # # Add grid
# # # plt.grid(True)

# # # # Show plot
# # # plt.show()

# # import matplotlib.pyplot as plt

# # # Sample data
# # size = [1000, 1500, 2000, 2500, 3000]
# # bedrooms = [2, 3, 3, 4, 5]
# # price = [200, 300, 400, 500, 600]  # in $1000s

# # plt.figure(figsize=(8, 6))

# # # Color represents the price
# # scatter = plt.scatter(size, bedrooms, c=price, cmap='viridis', s=100, edgecolor='k')

# # plt.title('House Size vs Bedrooms (Color = Price)')
# # plt.xlabel('Size (sq ft)')
# # plt.ylabel('Number of Bedrooms')

# # # Add color bar
# # plt.colorbar(scatter, label='Price ($1000s)')

# # plt.grid(True)
# # plt.show()


# # import matplotlib.pyplot as plt

# # # Sample data
# # num_links = [1, 2, 5, 0, 3, 7, 8, 1, 2, 6]
# # email_length = [100, 120, 60, 130, 80, 50, 40, 110, 115, 55]
# # labels = [0, 0, 1, 0, 1, 1, 1, 0, 0, 1]  # 0 = Not Spam, 1 = Spam

# # # Separate spam and not spam data
# # spam_x = [num_links[i] for i in range(len(labels)) if labels[i] == 1]
# # spam_y = [email_length[i] for i in range(len(labels)) if labels[i] == 1]

# # notspam_x = [num_links[i] for i in range(len(labels)) if labels[i] == 0]
# # notspam_y = [email_length[i] for i in range(len(labels)) if labels[i] == 0]

# # # Plot
# # plt.scatter(notspam_x, notspam_y, color='green', label='Not Spam', s=100, edgecolor='k')
# # plt.scatter(spam_x, spam_y, color='red', label='Spam', s=100, edgecolor='k')

# # plt.title('Spam vs Not Spam Emails')
# # plt.xlabel('Number of Links')
# # plt.ylabel('Email Length (words)')
# # plt.legend()
# # plt.grid(True)
# # plt.show()


# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Sample ML-like dataset
# data = {
#     'num_links': [1, 2, 5, 0, 3, 7, 8, 1, 2, 6],
#     'email_length': [100, 120, 60, 130, 80, 50, 40, 110, 115, 55],
#     'num_images': [0, 1, 3, 0, 1, 4, 5, 0, 1, 3],
#     'label': [0, 0, 1, 0, 1, 1, 1, 0, 0, 1]  # 0 = Not Spam, 1 = Spam
# }

# df = pd.DataFrame(data)
# print(df)
# # sns.set_style("whitegrid")

# # # 1. Count Plot - Class distribution
# # plt.figure(figsize=(5, 4))
# # sns.countplot(x='label', data=df)
# # plt.title("Class Distribution (Spam vs Not Spam)")
# # plt.xlabel("Label (0 = Not Spam, 1 = Spam)")
# # plt.ylabel("Count")
# # plt.show()

# # # 2. Box Plot - Distribution of num_links per class
# # plt.figure(figsize=(6, 5))
# # sns.boxplot(x='label', y='num_links', data=df)
# # plt.title("Number of Links by Label")
# # plt.xlabel("Label")
# # plt.ylabel("Num Links")
# # plt.show()

# # # 3. Violin Plot - Email length per class
# # plt.figure(figsize=(6, 5))
# # sns.violinplot(x='label', y='email_length', data=df)
# # plt.title("Email Length by Label")
# # plt.xlabel("Label")
# # plt.ylabel("Email Length")
# # plt.show()

# # 4. Scatter Plot - Email length vs num_links (colored by label)
# # plt.figure(figsize=(6, 5))
# # sns.scatterplot(x='num_links', y='email_length', hue='label', data=df, palette='Set1', s=100)
# # plt.title("Scatter: Links vs Length (Color = Label)")
# # plt.xlabel("Num Links")
# # plt.ylabel("Email Length")
# # plt.legend(title='Label')
# # plt.show()

# # 5. Heatmap - Feature Correlation Matrix
# plt.figure(figsize=(6, 4))
# sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
# plt.title("Feature Correlation Heatmap")
# plt.show()

# # # 6. Pair Plot - All feature interactions colored by class
# # sns.pairplot(df, hue='label', height=2.5, palette='husl')
# # plt.suptitle("Pair Plot (All Features)", y=1.02)
# # plt.show()
