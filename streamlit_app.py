import streamlit as st
import datetime
from st_supabase_connection import SupabaseConnection, execute_query
import smtplib
from email.message import EmailMessage

conn = st.connection("supabase",type=SupabaseConnection)

st.image("https://i0.wp.com/inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png?w=721&ssl=1")
st.title('Patch Report')
st.info('Fill out the form below')

with st.form("form"):
    engineer_name = st.text_input("Engineer Name*")
    engineer_email = st.text_input("Engineer Email Address*")
    engineer_contact_number = st.text_input("Engineer Phone Number*")
    location = st.text_input("Location*")
    location_contact_person = st.text_input("Location Contact Person")
    location_contact_number = st.text_input("Location Contact Number")
    image = st.file_uploader("Add Image", accept_multiple_files=True, type=['png', 'jpg', 'webp', 'jpeg'])
    status = st.selectbox('Status?',('Not Started', 'Completed', 'In Progress'))

    submit_button = st.form_submit_button("Submit")

    if submit_button:
        if engineer_name != "" and engineer_email != "" and engineer_contact_number != "" and location != "":
            
            st.success("Form submitted successfully!")

            msg = EmailMessage()
            subject = "Patch Report "+location+" "+status
            sender = "imbuzixjay@gmail.com"
            to = ["nxtgen@inmac.co.in", "support@inmac.co.in"]
            password = "aehl bovs lfaj lybs"
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender
            content = "New patch reported created\n\n\n\nEngineer: "+engineer_name+"\n\nEngineer Contact Number: "+engineer_contact_number+"\n\nEngineer Email: "+engineer_email+"\n\nLocation: "+location+"\n\nLocation Contact Number: "+location_contact_number+"\n\nLocation Contact Person: "+location_contact_person+"\n\nStatus: "+status+"\n\nImages in attachments"
            msg.set_content(content)
            images = []
            if image is not None:
                for i in image:
                    filename = "nextgen1/"+str(datetime.datetime.now())+i.__getattribute__("name")
                    conn.upload("images", "local",i , filename)
                    images.append(filename)
                    st.write(i.__getattribute__("name").split('.')[-1])
                    msg.add_attachment(i.read(), maintype='image', subtype=i.__getattribute__("name").split('.')[-1])

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender, password)
                msg['to'] = to
                smtp.send_message(msg)
                st.success("Email Sent!")


            execute_query(conn.table('nextgen1').insert([{"engineer_name":engineer_name,
                                                          "engineer_contact_number":engineer_contact_number,
                                                          "engineer_email":engineer_email,
                                                          "location":location,
                                                          "location_contact_person":location_contact_person,
                                                          "location_contact_number":location_contact_number,
                                                          "images":images,
                                                          "status":status}]), ttl='0')
        else: 
            st.warning("Fill all required fields.")
                

        
    
            
