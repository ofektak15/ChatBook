using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Data;
using System.Data.SqlClient;

public partial class Pages_Registration : System.Web.UI.Page
{
    // הפעולה בודקת האם שם המשתמש שהוכנס בהרשמה קיים כבר במערכת
    protected void Page_Load(object sender, EventArgs e)
    {
        if (IsPostBack)
        {
            string SQL = "SELECT COUNT (admin) FROM tblUsers WHERE userName='" +
                Request.Form["userName"] + "'";

            // Request.Form["userName"] שווה ל- userName ספירת כמה ערכים יש כאשר
            int count = (int)GetScalar(SQL);

            // אם המשתמש קיים כבר
            if (count == 1)
            {
                userName_Alert.InnerText = "User name is taken";
            }

            // אם המשתמש לא קיים
            else
            {
                // בניית השורה להוספה
                SQL = "INSERT INTO tblUsers (firstName, lastName, userName, password, Email, Telephone, Country, admin, birthday, Age, Gender) " +
                    "VALUES ('" + Request.Form["firstName"] + "', '" + Request.Form["lastName"] + "', '" + Request.Form["userName"] + "', '" + Request.Form["password"] +
                    "', '" + Request.Form["Email"] + "', '" + Request.Form["phone"] + "', '" + Request.Form["country_select"] +
                    "', 'false' " + ", '" + Request.Form["date"] + "', '" + Request.Form["age1"] + "', '" + Request.Form["gender2"] + "');";
                ExecuteNonQuery(SQL);

                // לאחר ההרשמה login העברה לדף ה
                Response.Redirect("Login2.aspx");
            }
        }
    }

    // SQL המייצגת את שאילתת ה SQL טענת כניסה: הפעולה מקבלת מחרוזת 
    // כששם המשתמש שווה לשם המשתמש שהוכנס בהרשמה admin טענת יציאה: הפעולה בודקת האם יש ערך בעמודה
    // ולכן המשתמש לא קיים admin אם הפעולה תחזיר אפס, זאת אומרת שאין בכלל ערך בעמודה
    // true/false יש ערך כלשהו שהוא יכול להיות admin אם הפעולה תחזיר 1, זה אומר שבעמודה 
    public object GetScalar(string SQL)
    {
        // התחברות למסד הנתונים
        string connectionString = @"Data Source = (LocalDB)\MSSQLLocalDB; AttachDbFilename = C:\Users\ofekt\Desktop\New_Site\newProject\newProject\App_Data\Database.mdf; Integrated Security = True";
        SqlConnection con = new SqlConnection(connectionString);

        // SQL בניית פקודת
        SqlCommand cmd = new SqlCommand(SQL, con);

        // ביצוע השאילתא
        con.Open();

        // ofek4 כששם המשתמש הוא admin אז הפעולה בודקת האם יש ערך כלשהו בעמודה ofek4 אם לדוגמה שם המשתמש שהוכנס הוא
        // מכיוון ששם משתמש זה הוא מנהל המערכת true היא admin הערך בעמודה ,ofek4 כאשר שם המשתמש הוא admin בעמודה 
        // הפעולה תחזיר 1 וכאשר הפעולה מחזירה אחד, זה אומר ששם המשתמש קיים כבר ,true מכיוון שבעמודה יש ערך כלשהו, שבמקרה הזה הוא
        object scalar = cmd.ExecuteScalar();
        con.Close();

        return scalar;
    }


    // SQL המייצגת את שאילתת ה SQL טענת כניסה: הפעולה מקבלת מחרוזת 
    // טענת יציאה: הפעולה מחזירה את מספר הרשומות שעודכנו ומעדכנת את טבלת המשתמשים בהתאם
    // הפעולה תמיד תחזיר את הערך 1 כי תמיד אנחנו מוסיפים רק משתמש אחד בהרשמה
    public int ExecuteNonQuery(string SQL)
    {
        // התחברות למסד הנתונים
        string connectionString = @"Data Source = (LocalDB)\MSSQLLocalDB; AttachDbFilename = C:\Users\ofekt\Desktop\New_Site\newProject\newProject\App_Data\Database.mdf; Integrated Security = True";
        SqlConnection con = new SqlConnection(connectionString);

        // SQL בניית פקודת
        SqlCommand cmd = new SqlCommand(SQL, con);

        // ביצוע השאילתא
        con.Open();
        int n = cmd.ExecuteNonQuery(); // מחזיר את מספר הרשומות שעודכנו
        con.Close();

        return n;
    }
}