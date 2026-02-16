import os

PO_FILE = 'locale/uz/LC_MESSAGES/django.po'

translations = {
    "Profile": "Profil",
    "Logout": "Chiqish",
    "Dashboard": "Boshqaruv Paneli",
    "My Profile": "Mening Profilim",
    "Member": "A'zo",
    "Contact Information": "Bog'lanish Ma'lumotlari",
    "Email": "Email",
    "Phone": "Telefon",
    "Address": "Manzil",
    "Edit Profile": "Profilni Tahrirlash",
    "Personal Details": "Shaxsiy Ma'lumotlar",
    "User Information": "Foydalanuvchi Ma'lumotlari",
    "First Name": "Ism",
    "Last Name": "Familiya",
    "Email Address": "Email Manzili",
    "Extended Profile": "Kengaytirilgan Profil",
    "Phone Number": "Telefon Raqami",
    "Location / Address": "Joylashuv / Manzil",
    "Bio": "Tarjimayi Hol",
    "Brief description about yourself.": "O'zingiz haqingizda qisqacha.",
    "Profile Picture": "Profil Rasmi",
    "Save Changes": "O'zgarishlarni Saqlash",
    "Certificates & Awards": "Sertifikatlar va Mukofotlar",
    "Add": "Qo'shish",
    "Are you sure you want to delete this certificate?": "Sertifikatni o'chirishga ishonchingiz komilmi?",
    "Issued:": "Berilgan:",
    "Expires:": "Amal qiladi:",
    "No certificates yet.": "Hozircha sertifikatlar yo'q.",
    "Add first certificate": "Birinchi sertifikatni qo'shish",
    "Login - Academic OS": "Kirish - Academic OS",
    "Sign in to your account": "Hisobingizga kiring",
    "Invalid username or password.": "Noto'g'ri foydalanuvchi nomi yoki parol.",
    "Username": "Foydalanuvchi nomi",
    "Enter your username": "Foydalanuvchi nomini kiriting",
    "Password": "Parol",
    "Enter your password": "Parolni kiriting",
    "Sign In": "Kirish",
    "Reports - Academic OS": "Hisobotlar - Academic OS",
    "All Reports (Admin)": "Barcha Hisobotlar (Admin)",
    "My Reports": "Mening Hisobotlarim",
    "Reports List": "Hisobotlar Ro'yxati",
    "Submit Report": "Hisobot Topshirish",
    "Teacher": "O'qituvchi",
    "Subject": "Fan",
    "Type": "Tur",
    "Status": "Holat",
    "Date": "Sana",
    "Actions": "Amallar",
    "Comment:": "Izoh:",
    "Approved": "Tasdiqlandi",
    "Rejected": "Rad etildi",
    "Under Review": "Tekshiruvda",
    "Download": "Yuklash",
    "Approve": "Tasdiqlash",
    "Reject": "Rad etish",
    "No reports yet.": "Hozircha hisobotlar yo'q.",
    "Approve Report": "Hisobotni Tasdiqlash",
    "Are you sure you want to approve this report?": "Ushbu hisobotni tasdiqlaysizmi?",
    "Yes, Approve": "Ha, Tasdiqlash",
    "Reject Report": "Hisobotni Rad etish",
    "Reason for Rejection:": "Rad etish sababi:",
    "Leave a comment about errors...": "Xatoliklar haqida izoh qoldiring...",
    "Cancel": "Bekor qilish",
    "Orders - Academic OS": "Buyruqlar - Academic OS",
    "Internal Orders Archive": "Ichki Buyruqlar Arxivi",
    "Orders List": "Buyruqlar Ro'yxati",
    "New Order": "Yangi Buyruq",
    "Number": "Raqam",
    "File": "Fayl",
    "No orders uploaded yet.": "Hozircha buyruqlar yuklanmagan.",
    "Observation Journal - Academic OS": "Kuzatuv Jurnali - Academic OS",
    "Mutual Lesson Observation Journal": "O'zaro Dars Kuzatuvi Jurnali",
    "Filters": "Filtrlar",
    "All": "Barchasi",
    "Start Date": "Boshlanish Sanasi",
    "End Date": "Tugash Sanasi",
    "Search": "Qidirish",
    "Observations Journal": "Kuzatuvlar Jurnali",
    "items": "ta",
    "Observer": "Kuzatuvchi",
    "Topic": "Mavzu",
    "Class": "Sinf",
    "Score": "Ball",
    "No observations found.": "Kuzatuvlar topilmadi.",
    "Clear Filters": "Filtrlarni tozalash",
    "Resource Center": "Resurs Markazi",
    "Educational Resources": "O'quv Resurslari",
    "Repository of study materials and documents.": "O'quv materiallari va hujjatlar ombori.",
    "Upload Resource": "Resurs Yuklash",
    "Title": "Sarlavha",
    "Description": "Tavsif",
    "Uploaded By": "Yuklagan",
    "Version": "Versiya",
    "Action": "Amal",
    "No file": "Fayl yo'q",
    "No resources found. Upload one to get started.": "Resurslar topilmadi. Boshlash uchun yuklang.",
    "My Tasks": "Mening Vazifalarim",
    "Tasks assigned to you or created by you.": "Sizga tayinlangan yoki siz yaratgan vazifalar.",
    "New Task": "Yangi Vazifa",
    "Priority": "Muhimlik",
    "Deadline": "Muddat",
    "High": "Yuqori",
    "Medium": "O'rta",
    "Low": "Past",
    "Completed": "Bajarildi",
    "In Progress": "Jarayonda",
    "Pending": "Kutilmoqda",
    "No tasks found. Click 'New Task' to get started!": "Vazifalar topilmadi. Boshlash uchun 'Yangi Vazifa' tugmasini bosing!",
    "History": "Tarix",
    "Record of all lesson observations.": "Barcha dars kuzatuvlari tarixi.",
    "New Observation": "Yangi Kuzatuv",
    "Methodist Dashboard": "Metodist Boshqaruv Paneli",
    "Methodist Dashboard - Academic OS": "Metodist Boshqaruv Paneli - Academic OS",
    "Total Observations": "Jami Kuzatuvlar",
    "Resources": "Resurslar",
    "Active Teachers": "Faol O'qituvchilar",
    "Top Teachers": "Eng Yaxshi O'qituvchilar",
    "Average Score": "O'rtacha Ball",
    "Recent Observations": "So'nggi Kuzatuvlar",
    "View All": "Barchasini ko'rish",
    "No statistics yet": "Hozircha statistika yo'q",
    "No observations yet": "Hozircha kuzatuvlar yo'q",
    "Quick Actions": "Tezkor Amallar",
    "All Observations": "Barcha Kuzatuvlar",
    "Lesson Details": "Dars Tafsilotlari",
    "Class Group": "Sinf",
    "Evaluation Criteria": "Baholash Mezonlari",
    "Submit Observation": "Kuzatuvni Yuborish",
    "Task Details": "Vazifa Tafsilotlari",
    "Back to List": "Ro'yxatga Qaytish",
    "High Priority": "Yuqori Muhimlik",
    "Medium Priority": "O'rta Muhimlik",
    "Low Priority": "Past Muhimlik",
    "Assignees": "Mas'ullar",
    "Edit Task": "Vazifani Tahrirlash",
    "Created By": "Yaratdi",
    "Created At": "Yaratilgan Vaqt",
    "Dependencies": "Bog'liqliklar",
    "Save Task": "Vazifani Saqlash",
    "Create Task": "Vazifa Yaratish",
    "Observations": "Kuzatuvlar",
    "Tasks": "Vazifalar",
    "Reports": "Hisobotlar",
    "Orders": "Buyruqlar",
}

def populate_po():
    if not os.path.exists(PO_FILE):
        print(f"File not found: {PO_FILE}")
        return

    with open(PO_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    updated_count = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        if line.startswith('msgid "'):
            msgid = line.strip()[7:-1] # Extract text inside quotes
            # Handle potential escaping in msgid
            msgid = msgid.replace('\\"', '"') 
            
            # Check the next line for msgstr
            if i + 1 < len(lines) and lines[i+1].startswith('msgstr ""'):
                # Check if we have a translation
                if msgid in translations:
                    trans_text = translations[msgid].replace('"', '\\"') # Escape quotes for po file
                    new_lines.append(f'msgstr "{trans_text}"\n')
                    i += 2 # Skip original msgstr "" line
                    updated_count += 1
                    continue
                elif msgid.strip() == "":
                    # Header msgid "", skip
                    pass
                else:
                    # Provide an empty translation if known
                    # Or keep as is
                    pass
        i += 1
            
    with open(PO_FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Updated {updated_count} translations in {PO_FILE}")

if __name__ == "__main__":
    populate_po()
