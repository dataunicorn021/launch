import streamlit as st
import random
from faker import Faker
import pandas as pd
from datetime import datetime
import math
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Initialize Faker for generating fake data
fake = Faker()

# Set a specific random seed (change this value as needed)
random_seed = 23
random.seed(random_seed)

##### DATA

# Create an empty DataFrame to store customer data
data = {
    'Company': [],
    'Plan': [],
    'Volume': [],
    'Phone': [],
    'Email': [],
    'Contact': [],
    'Area Code': [],
    'Signup Date': [],
    'Affiliate Status': [],
    'Usage Frequency': [],
    'Response Rate': [],
    'Revenue': [],
    'Churn Score': []
}

# Define Plans and their respective maximum volume limits
plans = ['Lite', 'Core', 'Pro']
plan_max_volumes = {
    'Lite': 10000,
    'Core': 20000,
    'Pro': 50000
}

# Define 7 different random ZIP codes
random_zip_codes = [fake.zipcode().split('-')[0] for _ in range(7)]

# Define monthly subscription prices for each plan
plan_prices = {
    'Lite': 497,
    'Core': 797,
    'Pro': 1497
}

# Calculate the start and end date range for signup_date
start_date = datetime(2019, 1, 1)
end_date = datetime.today()

# Define Churn Score calculation (based on Usage Frequency and Response Rate)
def calculate_churn_score(usage_frequency, response_rate):
    # Higher usage frequency and response rates result in a lower churn score
    churn_score = round(1 - (0.55 * usage_frequency + 0.45 * response_rate),2) * 100
    return churn_score

# Calculate Revenue based on plan and signup date
def calculate_revenue(plan, signup_date):
    subscription_price = plan_prices[plan]
    # Convert signup_date to datetime object
    signup_date = datetime.combine(signup_date, datetime.min.time())
    # Calculate the number of months since signup date and round it down
    months_since_signup = math.floor((datetime.today() - signup_date).days / 30)
    revenue = subscription_price * months_since_signup
    return revenue

# Generate 30 random customers
revenue_values = []


for _ in range(30):
    company_name = fake.company()
    plan = random.choice(plans)

    # Randomly generate volume within the specified maximum limit for the selected plan
    max_volume = plan_max_volumes[plan]
    volume = random.randint(1, max_volume)

    # Select a random ZIP code from the predefined list
    area_code = random.choice(random_zip_codes)

    # Generate a random US-style phone number (e.g., (123) 456-7890)
    phone_number = f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"

    email = fake.email()
    contact_name = fake.name()

    # Generate a random signup date between January 1, 2019, and today
    signup_date = fake.date_between(start_date=start_date, end_date=end_date)

    affiliate_status = random.choice(['Yes', 'No'])

    # Generate random values for Usage Frequency (range: 0-1) and Response Rate (range: 0-1)
    usage_frequency = round(random.uniform(0, 1), 2)
    response_rate = round(random.uniform(0, 1), 2)

    # Calculate Revenue based on plan and signup date
    revenue = calculate_revenue(plan, signup_date)
    revenue_values.append(revenue)

    data['Company'].append(company_name)
    data['Plan'].append(plan)
    data['Volume'].append(volume)
    data['Phone'].append(phone_number)
    data['Email'].append(email)
    data['Contact'].append(contact_name)
    data['Area Code'].append(area_code)
    data['Signup Date'].append(signup_date)
    data['Affiliate Status'].append(affiliate_status)
    data['Usage Frequency'].append(usage_frequency)
    data['Response Rate'].append(response_rate)

# Calculate Churn Score based on parameters
for i in range(len(data['Company'])):
    usage_frequency = data['Usage Frequency'][i]
    response_rate = data['Response Rate'][i]
    churn_score = calculate_churn_score(usage_frequency, response_rate)
    data['Revenue'].append(revenue_values[i])
    data['Churn Score'].append(churn_score)

# Create a DataFrame from the generated data
df = pd.DataFrame(data)

###### GRAPHS ######

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ['Introduction', 'Distribution of Plans', 'Sign-ups per Month',
        'Distribution of Affiliate Status', 'Churn Score', 'Upsell Opportunities']
)

##### NUMBER OF CUSTOMERS

with tab1:
    # Display the total number of customers as a big number
    st.subheader("Introduction")

    st.caption("Welcome to the Customer Segmentation Analysis. In this section, we'll explore how our customers are segmented based on their subscription plans, affiliate status, and other relevant factors. By understanding these segments, we can tailor our efforts to reduce churn, identify upselling opportunities, and enhance our overall customer experience.")
    st.caption("Have you ever wondered how understanding our customer segments can help us reduce churn and improve our services?")
    st.caption("We'll start by examining the total number of customers, followed by a breakdown of customer plans and distribution.")
    st.caption("In this initial analysis tab, focus is on the critical business metric of the total number of \
               customers. The large, prominent number provides an immediate overview of the customer base, \
               making it easy to gauge the company's reach. It's important to note that, for the purpose of \
               this assignment, monthly data was not generated. However, in a real-world business context, \
               tracking the percentage change in customer count compared to the previous period would be a \
               valuable addition to understand growth trends.")
    st.markdown("")
    st.markdown("##### Total Number of Customers")

    # Get the total number of customers
    total_customers = len(df)

    # Create a figure with a large text annotation to display the total number of customers
    fig = go.Figure()

    fig.add_annotation(
        text=str(total_customers),
        x=0.5,
        y=0.5,
        showarrow=False,
        font_size=60,  # Increase font size for a bigger number
        font_color="rgb(100,108,252)",  # Plotly's default blueish-purple color
        xanchor='center',  # Center the text horizontally
        yanchor='middle',  # Center the text vertically
    )

    fig.update_layout(
        width=300,
        height=200,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="white",  # Set the background color
    )

    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig)

    st.markdown("")
    st.markdown("##### List of Customers")
    st.markdown("")
    st.dataframe(df['Company'], height=1100)

##### PLANS

with tab2: 
     # Count the distribution of plans for the bar chart
    plan_counts_bar = df['Plan'].value_counts().reset_index()
    plan_counts_bar.columns = ['Plan', 'Count']

    # Specify the custom order for plans
    custom_order = ['Lite', 'Core', 'Pro']

    # Change the order of plans based on the custom order
    plan_counts_bar['Plan'] = pd.Categorical(plan_counts_bar['Plan'], categories=custom_order, ordered=True)
    plan_counts_bar = plan_counts_bar.sort_values('Plan')

    # Count the distribution of plans for the donut chart
    plan_counts_donut = df['Plan'].value_counts().reindex(custom_order)
    st.subheader("Distribution of Plans")
    st.caption("This section visualizes the distribution of customer plans using both a bar chart and a donut \
            chart. The bar chart displays the number of customers in each plan category, with different colors \
            representing each plan. On the other hand, the donut chart provides a concise overview of the \
            plan distribution with percentages. Both charts have a clean white background for clarity.")
    # Create columns
    col1, col2 = st.columns(2)

    # Extract the colors used in the bar chart
    bar_chart_colors = px.colors.qualitative.Plotly[:len(custom_order)]

    with col1:
        # Create a Plotly bar chart for Plan distribution
        fig_bar_chart = px.bar(plan_counts_bar, x='Plan', y='Count', color='Plan', color_discrete_sequence=bar_chart_colors)
        # Update the layout to set the background color to white
        fig_bar_chart.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white')
        st.plotly_chart(fig_bar_chart, use_container_width=True)

    with col2:
        # Create a donut chart for Plan distribution with the same colors and custom order
        fig_donut_chart = px.pie(names=custom_order, values=plan_counts_donut.values, hole=0.5, color=custom_order, color_discrete_sequence=bar_chart_colors)
        # Set the legend title and order
        fig_donut_chart.update_traces(marker=dict(colors=bar_chart_colors))
        fig_donut_chart.update_layout(legend_title_text='Plan')
        st.plotly_chart(fig_donut_chart, use_container_width=True)

    st.caption("""
    ***Insight: The majority of our customers are on the "Lite" plan.***

    Implication: While the "Lite" plan may be popular due to its affordability, there's an opportunity to increase revenue by encouraging these customers to upgrade to the more feature-rich "Core" plan.

    Suggestions for Upselling "Lite" Plan Customers to "Core" Plan:
    - Personalized Recommendations: Implement personalized recommendation engines that analyze customer usage patterns. Use these insights to suggest the "Core" plan to "Lite" plan customers who are approaching their volume limits or who are showing interest in advanced features.
    - Limited-Time Promotions: Offer time-limited promotions or discounts to "Lite" plan customers who upgrade to the "Core" plan. This can create a sense of urgency and incentivize them to take action.
    - Trial Periods: Offer "Lite" plan customers a trial period of the "Core" plan, allowing them to experience the additional features firsthand. During the trial, provide support and guidance to ensure they make the most of the new features.
    - Segmented Email Campaigns: Segment your email marketing campaigns based on customer behavior. Send targeted emails to "Lite" plan customers, focusing on the benefits that matter most to them. For example, if they frequently approach their volume limits, emphasize the increased limits of the "Core" plan.
    - Customer Support Outreach: Proactively reach out to "Lite" plan customers with personalized recommendations based on their usage patterns. Offer to discuss their specific needs and how upgrading to the "Core" plan can address those needs.
    - Feedback and Listening: Continuously collect feedback from "Lite" plan customers. Use their input to improve the "Core" plan and address any pain points or concerns they may have about upgrading.
    """)
    
##### MONTHS

with tab3:    
    # Extract month and year from the Signup Date
    df['Month-Year'] = pd.to_datetime(df['Signup Date']).dt.strftime('%m-%Y')

    # Count sign-ups per month and fill missing months with zeros
    signups_per_month = df['Month-Year'].value_counts().reindex(pd.date_range(start='2019-01-01', end=df['Month-Year'].max(), freq='MS').strftime('%m-%Y'), fill_value=0)

    # Create a Plotly line chart for sign-ups per month
    st.subheader("Sign-ups per Month")

    st.caption("The chart displays the number of sign-ups per month over time. It extracts the month and year \
                from the signup date, counts the sign-ups for each month, and fills any missing months with zeros. \
               The resulting Plotly line chart provides insights into the trend of sign-ups over the months.")

    fig = px.line(x=signups_per_month.index, y=signups_per_month.values)
    fig.update_xaxes(title="Month-Year", tickangle=90, tickvals=signups_per_month.index, ticktext=signups_per_month.index)
    fig.update_yaxes(title="Sign-ups Count")

    # Set the width of the figure as a percentage of the screen width (e.g., 100%)
    st.plotly_chart(fig, use_container_width=True)

##### Affiliate

with tab4:
    # Display a basic donut chart showing the distribution of affiliate status
    st.subheader("Distribution of Affiliate Status")

    st.caption("The chart illustrates the distribution of affiliate status, displaying the percentages of \
               'Yes' and 'No' responses. It provides insights into the extent of affiliate participation among \
               customers.")

    affiliate_counts = df['Affiliate Status'].value_counts()

    # Calculate percentages
    percentages = (affiliate_counts / affiliate_counts.sum() * 100).round(1)

    # Define custom labels for "Yes" and "No" with their percentages
    labels = [f"Yes ({percentages['Yes']}%)", f"No ({percentages['No']}%)"]

    # Create a donut chart using Plotly Express with default settings
    fig = px.pie(values=affiliate_counts.values, names=labels,
                hole=0.4)

    # Display the basic donut chart in Streamlit
    st.plotly_chart(fig)

##### Churn

with tab5:
    # Define custom bin ranges and labels
    bin_ranges = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    bin_labels = [f"{bin_start}-{bin_end}" for bin_start, bin_end in zip(bin_ranges[:-1], bin_ranges[1:])]

    # Use the cut function to create a new column with bin labels
    df['Churn Score Range'] = pd.cut(df['Churn Score'], bins=bin_ranges, labels=bin_labels, right=False)

    # Count values in each bin range
    value_counts = df['Churn Score Range'].value_counts().reset_index()
    value_counts.columns = ['Churn Score Range', 'Count']

    # Sort the values by the bin labels
    value_counts = value_counts.sort_values(by='Churn Score Range')

    # Display a column chart
    st.subheader("Number of Customers in Each Churn Score Range")
    fig = px.bar(value_counts, x='Churn Score Range', y='Count', labels={'Count': 'Frequency'})
    st.plotly_chart(fig)

    # Churn groups


    # Define the bins and labels for Churn Score groups
    bins = [1, 20, 40, 60, 80, 100]
    labels = ['Champions', 'Healthy', 'Pay attention', 'Risky', 'Red zone']

    # Add a new column 'Churn Score Group' with the group labels
    df['Churn Score Group'] = pd.cut(df['Churn Score'], bins=bins, labels=labels, right=False)

    # Count the number of companies in each Churn Score group
    count_by_group = df['Churn Score Group'].value_counts().reset_index()
    count_by_group.columns = ['Churn Score Group', 'Count']

    # Define the custom order for 'Churn Score Group'
    custom_order = ['Champions', 'Healthy', 'Pay attention', 'Risky', 'Red zone']

    # Create a custom color scale for the bar chart
    color_scale = {
        'Champions': 'dodgerblue',
        'Healthy': 'mediumseagreen',
        'Pay attention': 'khaki',
        'Risky': 'darkorange',
        'Red zone': 'firebrick',
    }
    st.subheader("Number of Customers in Each Churn Score Group")
    st.caption('While the score ranges provide insights into potential churn rates, categorizing customers \
               into named groups adds a practical dimension to our analysis. It`s important to note that \
               the group ranges were established arbitrarily for the sake of this assignment, offering a \
               simplified representation of customer churn dynamics.')

    # Create a bar chart using Plotly Express
    
    fig = px.bar(
        count_by_group,
        x='Churn Score Group',
        y='Count',
        labels={'Count': 'Frequency'},
        color='Churn Score Group',
        color_discrete_map=color_scale,
        category_orders={'Churn Score Group': custom_order},
    )

    # Update the axis labels and chart title
    fig.update_xaxes(title='Churn Score Group')
    fig.update_yaxes(title='Frequency')
    fig.update_layout(showlegend=False)

    # Display the bar chart in Streamlit
    st.plotly_chart(fig)

    ##### Churn score breakdown
    st.subheader("Churn Score Parameters")
    st.caption('The Churn Score parameter in this analysis is determined by considering two primary factors for simplicity: Usage Frequency and Response Rate. These metrics offer valuable insights into customer churn, shedding light on customer engagement and retention. However, for a more comprehensive analysis, we may explore additional parameters such as customer demographics, engagement history, transaction behavior, customer support interactions, and even if the customer upgraded to a higher plan already. These supplementary factors can provide a deeper understanding of customer behavior and enhance our predictive capabilities.')
    # Create a DataFrame with values for Usage Frequency and Response Rate
    data = {
        'Category': ['Usage Frequency', 'Response Rate'],
        'Percentage': [55, 45],
    }

    # Create a donut chart using Plotly Express
    fig = px.pie(
        data,
        names='Category',
        values='Percentage',
        hole=0.5,
        color_discrete_sequence=['#4CAF50', '#FFA500'],  # Green for Usage Frequency, Orange for Response Rate
    )

    # Display the donut chart in Streamlit
    st.plotly_chart(fig)


with tab6:

    # Calculate the percentage of plan used and add it as a new column
    def calculate_percentage(row):
        plan = row['Plan']
        volume = row['Volume']
        max_volume = plan_max_volumes.get(plan, 0)  # Get the max volume for the plan, default to 0 if not found
        percentage = (volume / max_volume) * 100 if max_volume > 0 else 0
        return f"{percentage:.1f}%"  # Format as a string with 1 decimal place and '%' symbol

    df['Percentage of Plan Used'] = df.apply(calculate_percentage, axis=1)

    # Display the mini bar chart on the Streamlit page
    df['Percentage of Plan Used'] = df['Percentage of Plan Used'].str.rstrip('%').astype(float)

    # Sort the DataFrame by Percentage of Plan Used in descending order
    df = df.sort_values(by='Percentage of Plan Used', ascending=False)

    # Define a color for the bars
    bar_color = '#646cfc'

    # Create a Streamlit container
    st.subheader("Percentage of Plan Used")

    st.caption("While the dataset, created for simplicity, lacks monthly volume data, a graph illustrating \
               customers nearing their plan's maximum value could offer valuable insights for upselling \
               opportunities. It's important to note that, due to time constraints, the originally planned \
               slide selector for percentage ranges and drop-down menu for filtering customers per i.e. Plan were not included.")

    # Loop through the DataFrame to display horizontal bars and percentages
    for index, row in df.iterrows():
        company_name = row['Company']
        percentage = row['Percentage of Plan Used']
        
        # Create a container for the company name, bar, and percentage
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            # Display the company name
            st.write(company_name)
        
        with col2:
            # Display the horizontal bar
            st.markdown(
                f"""
                <div style="background-color: {bar_color}; height: 20px; width: {percentage}%;"></div>
                """
                , unsafe_allow_html=True)
        
        with col3:
            # Display the percentage on the right axis
            st.write(f"{percentage:.1f}%")
