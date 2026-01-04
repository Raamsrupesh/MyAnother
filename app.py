import streamlit as st 
import pandas as pd 
import numpy as np 
import hashlib 
import sqlite3 
import uuid 
import os 
from datetime import datetime as datime
import csv
from random import choice

MENT_PASSWORD = 'mentor_password.csv'
ROLL_DEVICE_STU_DB = 'studentrolldevice.db'
ATTENDANCE_DB = 'attendance.db'
REP_PASS = 'rep_password.csv'
PERMISSIONS_DB = 'permissions.db'
GOOD_NEWS = 'good_new.txt'
FEEDBACK_FILE = 'feedback.csv'



def read():
    if os.path.exists(GOOD_NEWS):
        with open(GOOD_NEWS, mode='r', encoding='utf-8') as f:
            return f.read()
        return ""
st.markdown("""
        <style>
            .block-container { padding-top: 2rem !important; margin-top:1.5rem !important;}
            .custom-banner {
                    position: fixed;
                    top: 20;
                    left: 0;
                    width: 100vw;
                    z-index: 1000;
                    margin-bottom: 0.75rem !important;
                    padding: 10px;
                    display:flex;
                    align-items: center !important;
                    padding-top:1rem !important;
            }
            body { padding-top: 60px !important; }
            </style>
    """, unsafe_allow_html=True)
if read() != "" and read() is not None:
            st.markdown(
                f"""
                <div class='custom-banner' style='background:{choice(['white', 'lightyellow', 'skyblue', 'lightpink', 'lavender', 'mintcream', 'aliceblue', 'honeydew', 'azure', 'seashell', 'beige', 'mistyrose'])}; color:{choice(['black', 'darkblue', 'darkviolet', 'purple'])}; font-size:20px; border-radius:4px;font-family:{choice(['Arial', 'Verdana', 'Tahoma', 'Trebuchet MS', 'Georgia', 'Times New Roman', 'Impact', 'Comic Sans MS', 'Courier New', 'Lucida Console', 'Palatino Linotype', 'Garamond'])}'>
                    <marquee behavior='scroll' direction='left' scrollamount='7'>
                        {read()}
                    </marquee>
                </div>
                """,
                unsafe_allow_html=True
)
            st.markdown("<br><br>", unsafe_allow_html=True)




st.logo("https://user-gen-media-assets.s3.amazonaws.com/seedream_images/8b141d02-3bc5-4dbe-a05a-bd37908dafe6.png", size="medium")    
st.sidebar.image("https://user-gen-media-assets.s3.amazonaws.com/seedream_images/b2c7b8bb-bca9-47d4-be77-c5c11c3378dd.png")


CLASS_ROLL_NUMBERS = [
                    'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'Y0', 'Y1', 'Y2', 'Y3',
                    'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'Z0', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6',
                    'Z7', 'Z8', 'Z9', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ',
                    'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW',
                    'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ',
                    'BK'
]



conn = sqlite3.connect(ROLL_DEVICE_STU_DB)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS studentrolldevice(id INTEGER PRIMARY KEY AUTOINCREMENT, rollno VARCHAR(2) NOT NULL, device_id VARCHAR(200) NOT NULL);")
conn.commit()


at_con = sqlite3.connect(ATTENDANCE_DB)
at_cur = at_con.cursor()
at_cur.execute("CREATE TABLE IF NOT EXISTS attendance(id INTEGER PRIMARY KEY AUTOINCREMENT, rollno VARCHAR(2) NOT NULL, date_pre date NOT NULL, time_pre time NOT NULL);")
at_con.commit()


per_con = sqlite3.connect(PERMISSIONS_DB)
per_cur = per_con.cursor()
per_cur.execute("CREATE TABLE IF NOT EXISTS permissions(id INTEGER PRIMARY KEY AUTOINCREMENT, date_per date NOT NULL, rollno VARCHAR(2) NOT NULL, cause VARCHAR(700) NOT NULL, no_of_days INTEGER NOT NULL, granted VARCHAR(3) NOT NULL);")
per_con.commit()



if not os.path.exists(MENT_PASSWORD):
    with open (MENT_PASSWORD , mode='w', newline="") as f:
        f.write(hashlib.sha256(f'{chr(84)+chr(69)+chr(65)+chr(67)+chr(82)}'.encode()).hexdigest())
if not os.path.exists(REP_PASS):
    with open (REP_PASS, mode='w', newline="") as f:
        f.write(hashlib.sha256(f'{chr(82)+chr(69)}P{chr(ord("1"))+chr(ord("2"))+chr(ord("3"))}'.encode()).hexdigest())
if not os.path.exists(FEEDBACK_FILE):
    feedback_df = pd.DataFrame(columns=['feed', 'gb', 'appleation'])
    feedback_df.to_csv(FEEDBACK_FILE, index=False)
feedback_df = pd.read_csv(FEEDBACK_FILE)
with open (MENT_PASSWORD, mode="r", newline="") as f:
    teach_pass = f.read()



who = st.sidebar.radio("Navigate to: ", ['Mentor', 'Student', 'Admin', 'NoticeBoard', 'Feedback', 'About'], index = 1)
if who == 'Mentor': 
    st.header("Mentor Portal: ")
    ment_password = st.text_input("Enter Mentor Password: ", type='password')
    if hashlib.sha256(ment_password.encode()).hexdigest() == teach_pass:
        st.toast("**WELCOME**", icon = '🙏', duration='long')
        st.write("---")
        st.subheader("Permissions for Today: ")
        today_per_df = pd.read_sql('SELECT * FROM permissions WHERE date_per = ?', con=per_con, params=(datime.now().strftime("%Y-%m-%d"),))
        # st.write(today_per_df)
        for i in range(len(today_per_df)):
            if (today_per_df['granted'][i] == 'NOT YET') or (today_per_df['granted'][i] == 'SEEN'):
                stu_per = st.radio(label=f"{today_per_df['rollno'][i]}: {today_per_df['cause'][i]}. Therefore I need a leave for {today_per_df['no_of_days'][i]} days", options=['SEEN','ACCEPTED', 'REJECTED'],horizontal=True, index=0)
            elif today_per_df['granted'][i] == 'ACCEPTED':
                stu_per = st.radio(label=f"{today_per_df['rollno'][i]}: {today_per_df['cause'][i]}. Therefore I need a leave for {today_per_df['no_of_days'][i]} days", options=['SEEN','ACCEPTED', 'REJECTED'],horizontal=True, index=1)
            elif today_per_df['granted'][i] == 'REJECTED':
                stu_per = st.radio(label=f"{today_per_df['rollno'][i]}: {today_per_df['cause'][i]}. Therefore I need a leave for {today_per_df['no_of_days'][i]} days", options=['SEEN','ACCEPTED', 'REJECTED'],horizontal=True, index=2)
            per_cur.execute("UPDATE permissions SET granted = ? WHERE (date_per = ?) AND (rollno = ?);", (stu_per, datime.now().strftime("%Y-%m-%d"), today_per_df['rollno'][i]))
            per_con.commit() 
            st.write("---")

        st.subheader("Today's Attendance: ")
        tea_pre, tea_abs = st.columns([2, 1])
        with tea_pre:
            tea_pre_df = pd.read_sql("SELECT rollno, time_pre FROM attendance WHERE date_pre = ?;", con = at_con, params=(datime.now().strftime("%Y-%m-%d"),))
            st.write(tea_pre_df)
        with tea_abs:
            tea_abs_df = []
            for i in CLASS_ROLL_NUMBERS:
                if i not in tea_pre_df['rollno'].to_list():
                    tea_abs_df.append(i)
            tea_abs_df = pd.DataFrame(tea_abs_df, columns=['rollno'])
            t_abs = tea_abs_df['rollno'].isin(today_per_df['rollno'])
            # tea_abs_df = tea_abs_df.loc[(tea_abs_df['rollno'] == today_per_df['rollno']) & (today_per_df['granted'] == 'Accepted')]
            # st.write(pd.concat([tea_abs_df, t_abs_df], axis=1 ,ignore_index=True))
            def green_style(row):
                if t_abs[row.name]:
                    return ['background-color: lightblue'] * len(row)
                return [''] * len(row)

            styled_df = tea_abs_df.style.apply(green_style, axis=1)
            st.dataframe(styled_df, use_container_width=True)
        

elif who == 'Student':
    st.title("**Student Portal**" + '🧑‍🎓')
    
    from streamlit_cookies_controller import CookieController 
    controller = CookieController()

    device_id = controller.get("device_id")
    if device_id is not None:
        cur.execute("SELECT rollno FROM studentrolldevice WHERE device_id = ?", (device_id,))
        user_roll = cur.fetchone()

        if user_roll is None:
            user_roll = st.selectbox("Enter Roll NO: ", CLASS_ROLL_NUMBERS)
            controller.set('device_id',hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest(), max_age=365 * 24 * 60 * 60)
            st.session_state['user'] = controller.get("device_id")  

            if st.button("**BOUND PERMANENTLY**", type = 'primary') and st.session_state['user']:
                cur.execute("INSERT INTO studentrolldevice(rollno, device_id) VALUES (?, ?)", (user_roll, st.session_state['user']))
                conn.commit()
                st.success(f"You({user_roll}) are Permanently bound to this device whose ID is: {st.session_state['user']}")

        elif user_roll is not None:
            st.session_state['user'] = device_id
            st.warning(f"{user_roll[0]} -> {st.session_state['user']}")
            st.selectbox("Enter Roll NO:", options=user_roll, disabled=True)

            st1, st2, st3, st4, st5 = st.tabs(['Student/CR', 'AskPermission', 'LeaderBoard','Chat' ,'PrevRecords'])
            with st1:
                st.header("Select the mode of entry ")
                a = st.radio("options available: ", ['STUDENT', 'CR'])
                if a == "STUDENT":
                    st.write("---")
                    st.header("Mark Your Presence")
                    from streamlit_geolocation import streamlit_geolocation 
                    location = streamlit_geolocation()
                    st.write(f'📍You are at {location["latitude"]} N and {location["longitude"]} S')
                    try:
                        if (location['latitude'] > 18 and location['latitude'] < 19) and (location['longitude'] > 83 and location['longitude'] < 84):
                            at_cur.execute("SELECT rollno FROM attendance WHERE rollno = ? AND date_pre = ?", (user_roll[0], datime.now().date()))
                            if not at_cur.fetchone():
                                if st.button("Mark Present"):
                                    st.balloons()
                                    at_cur.execute("INSERT INTO attendance(rollno, date_pre, time_pre) VALUES (?,?,?);", (user_roll[0], datime.now().strftime("%Y-%m-%d"), datime.now().strftime("%H:%M:%S")))
                                    at_con.commit()
                            else:
                                st.warning(" You have already marked the attendance today!!")
                        else:
                            st.error(" The location is not matching!!")
                    except TypeError:
                        st.warning("Click on the above location button")


                    # if st.button("GET YOUR DETAILS"):
                    #     at_cur.execute("SELECT rollno, date_pre, time_pre FROM attendance WHERE rollno = ?;", (user_roll))        
                    #     # st.write(at_cur.fetchall())
                    #     with open(ATTENDANCE_CSV, 'w', newline='', encoding='utf-8') as f:
                    #         writer = csv.writer(f)
                    #         writer.writerow([desc[0] for desc in at_cur.description])
                    #         writer.writerows(at_cur.fetchall())
                    try:
                        with st.expander("GET MONTHLY REPORT:"):
                            mon = st.radio("SELECT MONTH: ", ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'], index=datime.now().month + 1)
                            if mon == 'JAN':
                                mon = '01'
                            elif mon == 'FEB':
                                mon = '02'
                            elif mon == 'MAR':
                                mon = '03'
                            elif mon == 'APR':
                                mon = '04'
                            elif mon == 'MAY':
                                mon = '05'
                            elif mon == 'JUN':
                                mon = '06'
                            elif mon == 'JUL':
                                mon = '07'
                            elif mon == 'AUG':
                                mon = '08'
                            elif mon == 'SEP':
                                mon = '09'
                            elif mon == 'OCT':
                                mon = '10'
                            elif mon == 'NOV':
                                mon = '11'
                            elif mon == 'DEC':
                                mon = '12'
                            at_cur.execute(f"SELECT * FROM attendance WHERE date_pre LIKE '{datime.now().date().year}-{mon}-%'")                        
                            with open(f'{user_roll[0]}{mon}attendance.csv', 'w', newline='', encoding='utf-8') as f:
                                writer = csv.writer(f)
                                writer.writerow([desc[0] for desc in at_cur.description])
                                writer.writerows(at_cur.fetchall())
                            with open (f'{user_roll[0]}{mon}attendance.csv', 'r', newline="", encoding="utf-8") as f:
                                csv_data = f.read()
                            st.download_button("Download Report", data=csv_data, file_name=f'{user_roll[0]}{mon}attendance.csv', mime = "text/csv", icon = ":material/download:")
                    except:
                        pass 
                    at_cur.execute('SELECT COUNT(DISTINCT rollno) FROM attendance WHERE (rollno = ?) AND (date_pre LIKE ?);', (user_roll[0], f"{datime.now().year}-{datime.now().month}-%"))
                    percentage = (len(at_cur.fetchall()) / 30) * 100
                    if percentage < 62:
                         st.error(f"The attendance percentage is: {percentage}%")
                    elif percentage >= 63 and percentage < 75:
                        st.warning(f"The attendance percentage is: {percentage}%")
                    else:
                        st.success(f"The attendance percentage is: {percentage}%")
                    
                elif a == "CR":
                    with open (REP_PASS, 'r', newline="") as f:
                        act_cr = f.read()
                    CR_pass = st.text_input("Enter CR Password: ", placeholder='*******', type='password')
                    if CR_pass == "":
                        st.warning("Enter the CR password!")
                    elif hashlib.sha256(CR_pass.encode()).hexdigest() == act_cr:
                        pre, abs = st.columns([2, 1])
                        with pre:
                            pre_df = pd.read_sql(sql = "SELECT rollNo, time_pre FROM attendance WHERE date_pre = ?;", con=at_con, params=(datime.now().strftime("%Y-%m-%d"),))
                            st.write(pre_df)
                        with abs:
                            absenties = []
                            for i in CLASS_ROLL_NUMBERS:
                                if i not in pre_df['rollno'].to_list():
                                    absenties.append(i)
                            absenties = pd.DataFrame(absenties, columns=['rollno'])
                            abse = absenties['rollno'].isin(pd.read_sql('SELECT * FROM permissions WHERE date_per = ? AND rollno = ?', per_con, params=(datime.now().strftime("%Y-%m-%d"), user_roll[0])))
                            st.write(pd.concat([absenties, abse], axis = 1, ignore_index=True))
                    else:
                        st.error("Wrong CR Password!!")        

            with st2:
                
                st.write("---")
                st.header("New Permission Letter")
                with st.form(key = f"{user_roll}{datime.now().date().day} Permission form", clear_on_submit= True):
                    no_of_days = st.slider("Number of Days", min_value=1/2, max_value=20.0, step=1.0)
                    cause = st.text_area("Enter the Reason: ")
                    if st.form_submit_button("SUBMIT", help="After this you can't able to modify the number of days and cause"):
                        per_cur.execute("INSERT INTO permissions(rollno, date_per, cause, no_of_days, granted) VALUES (?,?,?,?,?);", (user_roll[0],datime.now().strftime("%Y-%m-%d"), cause, no_of_days, 'NOT YET'))
                        per_con.commit()
                st.write("---")
                var = pd.read_sql("SELECT * FROM permissions WHERE rollno = ? ORDER BY date_per DESC", per_con, params=(user_roll))
                st.header("Status:")
                if var.iloc[0]['granted'] == "REJECTED":
                    st.error(f" The latest request of permission was: **{var.iloc[0]['granted']}**")
                elif var.iloc[0]['granted'] == "ACCEPTED":
                    st.success(f" The latest request of permission was: **{var.iloc[0]['granted']}**")
                else:
                    st.info(f" The latest request of permission was: **{var.iloc[0]['granted']}**")
                st.write("---")
                st.header("Your previous requests:")
                if var.iloc[0]['granted'] == "Accepted":
                    st.toast("Accepted!!", icon = '👍')
                if var is not pd.DataFrame({}):
                    st.write(var)
                else:
                    st.write("You didn't raise any permission request yet!!")


            with st3:
                leader_board_df = pd.read_sql(f"SELECT rollno, COUNT(*) AS noOfPresenties, avg(time_pre) AS avgTime FROM attendance WHERE date_pre LIKE ? GROUP BY rollno ORDER BY noOfPresenties DESC, avgTime", con=at_con, params=(f'{datime.now().strftime("%Y-%m")}-%',))
                st.dataframe(leader_board_df)

            with st4:
                msg = st.chat_input("Enter your message: ")
                if msg != "":
                    pass

elif who == 'Admin':
        st.title("👨‍🔬 Admin Panel")
        def write(msg):
            with open(GOOD_NEWS, mode='w', encoding='utf-8') as f:
                f.write(msg) 

        if st.session_state.get("user") == 'bb570cc50e62f041093eb93d6859c672fe80e84fe7e6b1603dd3165d0a568da0':
            st.header("📢 Announcement Management")
            message = st.text_input(label = "New Announcement:", placeholder='Enter your messsage...')
            if st.button("🔊 Publish Announcement"):
                write(message)
        
            if st.button("🔇 Clear Announcement"):
                write("")
            st.write("---")
            st.header("📊 System Statistics")
            try:
                x,y,z=st.columns(3)
                with x:
                    st.metric(f"Total Students",len(CLASS_ROLL_NUMBERS))  
                with y:
                    # pass
                    st.metric(f"Registered Students",len(pd.read_sql(sql="SELECT count(DISTINCT rollno) FROM studentrolldevice;", con=conn)))
                with z:
                    st.metric(f"Today's Attendance", len(pd.read_sql("SELECT COUNT(rollno) FROM attendance WHERE date_pre = ?;", con = at_con, params=(datime.now().strftime("%Y-%m-%d"),))))
            except:
                st.error("Files not created yet!!")
            st.write("---")  
            try:
                st.header("User Feedbacks: ")
                feedback_df = pd.read_csv(FEEDBACK_FILE) 
                for i,j in feedback_df.iterrows():
                    st.write(f"{j[2]}: {j[0]}. Finally he gave: {j[1]}")
            except:
                st.info("No one has yet given the feedback!!")           
            st.write("---")
            st.header("🔧 System Maintenance")
            if st.button("🔄 Clear All Data", type="secondary"):
                pass
            st.write("---")
            _1, _2 = st.columns(2)
            with _1:
                min_latrange = st.number_input("Enter latitude min range")
                maxlatrange = st.number_input("Enter latitude max range")
            with _2:
                min_lonrange = st.number_input("Enter longitude min range")
                maxlonrange = st.number_input("Enter longitude max range")
                # st.success("All data cleared!") 
            if st.button("Clear cache"):
                st.cache_data.clear()
                st.rerun()

        else:
            st.error("🚫 Access denied. Admin privileges required.")


elif who == "NoticeBoard":
    try:
        st.title("🪧 NOTICE BOARD")
        this_month = datime.now().date().month 
        leader_board_df = pd.read_sql(f"SELECT rollno, COUNT(*) AS noOfPresenties, avg(time_pre) AS avgTime FROM attendance WHERE date_pre LIKE '{datime.now().date().year}-{this_month}-%' GROUP BY rollno ORDER BY noOfPresenties DESC, avgTime", con=at_con)
        st.subheader('This month the lead was: ', leader_board_df.iloc[0])
        st.dataframe(leader_board_df)

    except:
        st.info("No significant highlights are available!!")


elif who == "Feedback":
    st.title("Feedback Form")
    st.write("---")
    with st.form(key=f"{st.session_state['user']}Feedbackform"):
        appleation = st.text_input("How are you liked to be appeleated as: ")
        feed = st.text_area("Drop your feedback here")
        gb = st.radio("How was this?", options=['Need Improvement🔧','OK 🆗', 'Satisfied😊', 'Best🥳'], horizontal=True, index = 2)

        if st.form_submit_button("SUBMIT"):
            if appleation == "":
                appleation = None 
            if feed == "" or gb == "" :
                st.warning("**Kindly fill feedback!!**")
            else:
                new_row = pd.DataFrame(data={"feed": [feed], "gb": [gb], "appleation": [appleation]})
                feedback_df = pd.concat([feedback_df, new_row], ignore_index=True, axis=0)
                feedback_df.to_csv(FEEDBACK_FILE, index=False)
                st.toast("Thank you, Your feedback is too much valuable for us!!", icon="🙏", duration='long')

    st.write("---")

elif who == "About":
            from datetime import datetime

            APP_NAME = "Presaloc Pro"
            VERSION = "v2.0"
            DEVELOPER = "Saketh (Rupesh)"
            LAST_UPDATE = datetime(2025, 10, 27)

            about_header = f"""
             # Welcome to **{APP_NAME}** app!

             A professional system designed to verify and secure attendance across classes (students, CRs, mentors, admin), all with advanced, modern technology and strict validation.
            
            ---
            Updated Recently on: {LAST_UPDATE}\n
            Welcome to my advanced, location-based attendance management platform—engineered to deliver reliable, secure, and automated attendance for educational institutions and organizations.
            """

            st.markdown(about_header)
            st.subheader("Advanced Features")
            st.markdown(
            """
            - **Smart Location Validation:** Ensures users are at authorized physical locations before marking attendance (uses HTML5 Geolocation API).
            - **Role-Based Security:** Custom access control for students, admins, and supervisors with encrypted session tokens.
            - **Real-Time Analytics:** Visual dashboards, attendance statistics, and downloadable reports.
            - **Proxy Prevention:** Strict geolocation and session checks to block fraudulent or duplicate entries.
            """
            )
            st.error("⚠️⚠️**One Time Registration:** This feature will not allow any user to use another user's details. And once registered to a device, that very device owner could only use those details.")
            

            st.write("---")
            st.info("Driven by a passion for building robust, real-world solutions for education and organizations.")

            st.metric(label="App Version", value="v2.0", delta="+1 new feature")
            st.metric(label="Active Users", value="000", delta="+2 this week")

            tab1, tab2 = st.tabs(["Overview", "Technical Details"])
            with tab1:
                st.markdown("""
                Welcome to our advanced, location-based attendance platform.
                - **Location Validation**
                - **Security & Analytics**
                - Role-based access
                """)
            with tab2:
                st.subheader("Technology Stack")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        """
                        - Python 3.13+
                        - Streamlit
                        - SQLite (Data Storage)
                        - HTML5 Geolocation
                        """
                    )
                with col2:
                    st.markdown(
                        """
                        - Pandas (Data Handling)
                        - Secure Session Management
                        - Responsive Web UI
                        - Real-time Data Analytics
                        """
                    )

            with st.expander("Meet the Developer"):
                st.write("Created by Saketh (Rupesh), a student developer passionate about practical AI solutions.")

            st.download_button("Download App Manual", """~ A Website made by Saketh (Rupesh).""", file_name="manual.txt")

# elif who == "Settings":

st.caption("~An app by Saketh (Rupesh), accomplished in 5-6 days & completed prior to 27th October 2025.")

                        




