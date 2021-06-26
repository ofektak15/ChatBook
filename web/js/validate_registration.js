function validate_registration_form() {
    var name = document.forms["registration_form"]["firstName"].value; // שם פרטי
    var LastName = document.forms["registration_form"]["lastName"].value; // שם משפחה
    var phone = document.forms["registration_form"]["Phone"].value; // מספר טלפון
    var userName = document.forms["registration_form"]["UserName"].value; // שם משתמש
    var password = document.forms["registration_form"]["Password"].value; // סיסמה
    var MediumPassword = document.forms["registration_form"]["Password"].value; // סיסמה בינונית
    var StrongPassword = document.forms["registration_form"]["Password"].value; // סיסמה חזקה
    var confirmPassword = document.forms["registration_form"]["confirmPassword"].value; // אימות סיסמה
    var email = document.forms["registration_form"]["Email"].value; // אימייל
    // var response = grecaptcha.getResponse(); // האם רובוט
    var gender = document.getElementsByName("gender"); // מגדר
    var country = document.getElementById("country_select").value; // מדינה
    var age = document.forms["registration_form"]["age"].value; // גיל
    var date = document.getElementById("date").value; // תאריך לידה


    var mode = checkName(name);
    var status_registration = false;

    mode = checkLastName(LastName) && mode;

    mode = checkPhone(phone) && mode;

    mode = checkUserName(userName) && mode;

    mode = checkPassword(password, MediumPassword, StrongPassword) && mode;

    mode = checkConfirmPassword(password, confirmPassword) && mode;

    mode = checkEmail(email) && mode;

    // mode = checkRobot(response) && mode;

    mode = checkRadio(gender) && mode;

    mode = checkCountry(country) && mode;

    mode = checkAge(age) && mode;

    mode = checkDateBirth(date) && mode;

        // TODO: different errors for failed registration and failed checks
        // should be mode == true
    if (true){
        alert("Attempting to register...");
//        status_registration = eel.register()();
        status_registration = eel.register(userName, password);
        // status_registration = eel.register(userName, password);
        alert("???");
        return status_registration;
    }
    else{
        alert("Please fix the form :)");
        // TODO: Should redirect to login if registration succeeded
        window.location.href="127.0.0.1:8080/login.html";
    }
    return mode;
}




// בדיקת שם פרטי
function checkName(name) {

    var containOnlyLetters = true; // משתנה בוליאני שבודק האם יש רק אותיות בשם

    // בדיקה האם המשתמש הכניס שם פרטי
    if (name.length == 0) {
        document.getElementById("error_first_name").innerHTML = "You must fill out this field";
        return false;
    }

    // בדיקה האם המשתמש הכניס רק אותיות
    for (var i = 0; i < name.length; i++) {
        if (!(name[i] >= 'a' && name[i] <= 'z' || name[i] >= 'A' && name[i] <= 'Z')) {
            containOnlyLetters = containOnlyLetters && (name[i] >= 'a' && name[i] <= 'z' || name[i] >= 'A' && name[i] <= 'Z');
        }
    }
    if (containOnlyLetters == false) {
        document.getElementById("error_first_name").innerHTML = "Name must contain only letters";
        return false
    }


    // בדיקה האם המשתמש הכניס רק אות אחת
    if (name.length < 2) {
        document.getElementById("error_first_name").innerHTML = "Name must be more than 1 letter";
        return false;
    }

    document.getElementById("error_first_name").innerHTML = "";
    return true;
}

// בדיקת שם משפחה
function checkLastName(LastName) {

    var containOnlyLetters = true; // משתנה בוליאני שבודק האם יש רק אותיות בשם משפחה

    // אם המשתמש לא הכניס את שם המשפחה
    if (LastName.length == 0) {
        document.getElementById("error_last_name").innerHTML = "You must fill out this field";
        return false;
    }


    // בדיקה האם המשתמש הכניס רק אותיות
    for (var i = 0; i < LastName.length; i++) {
        if (!(LastName[i] >= 'a' && LastName[i] <= 'z' || LastName[i] >= 'A' && LastName[i] <= 'Z')) {
            containOnlyLetters = containOnlyLetters && (LastName[i] >= 'a' && LastName[i] <= 'z' || LastName[i] >= 'A' && LastName[i] <= 'Z');
        }
    }
    if (containOnlyLetters == false) {
        document.getElementById("error_last_name").innerHTML = "Name must contain only letters";
        return false
    }


    // אם המשתמש הכניס רק אות אחת
    if (LastName.length < 2) {
        document.getElementById("error_last_name").innerHTML = "Last name must be more than 1 letter";
        return false;
    }
    document.getElementById("error_last_name").innerHTML = "";
    return true;
}

// בדיקת מספר טלפון
function checkPhone(phone) {
    var thirdDigit = phone[2]; // הסיפרה השלישית
    var containOnlyNumbers = true; // משתנה בוליאני שבודק האם מספר הטלפון כולל רק מספרים

    // בדיקה האם המשתמש הכניס את מספר הטלפון
    if (phone.length == 0) {
        document.getElementById("error_phone_number").innerHTML = "You must fill out this field";
        return false;
    }

    // בדיקה האם המשתמש הכניס רק מספרים
    for (var i = 0; i < phone.length; i++) {
        containOnlyNumbers = containOnlyNumbers && (phone[i] >= 0 && phone[i] <= 9);
    }
    if (containOnlyNumbers == false) {
        document.getElementById("error_phone_number").innerHTML = "Phone number must contain only numbers";
        return false;
    }


    // אם 2 הספרות הראשונות הן לא 0 ו-5
    if (phone[0] != 0 || phone[1] != 5) {
        document.getElementById("error_phone_number").innerHTML = "Phone number must start with 05!";
        return false;
    }
    // אם אורך המחרוזת גדול מ-10
    else if (phone.length > 10) {
        document.getElementById("error_phone_number").innerHTML = "Phone number can not be more than 10 numbers";
        return false;
    }
    // אם אורך המחרוזת קטן מ-10
    else if (phone.length < 10) {
        document.getElementById("error_phone_number").innerHTML = "Phone number can not be less than 10 numbers";
        return false;
    }

    // אם הסיפרה השלישית היא לא 0,2,4,5,8
    if ((thirdDigit == 0) || (thirdDigit == 2) || (thirdDigit == 4) || (thirdDigit == 5) || (thirdDigit == 8)) {
        document.getElementById("error_phone_number").innerHTML = "";
        return true;
    }
    else {
        document.getElementById("error_phone_number").innerHTML = "Third digit must contain one of these : 0,2,4,5,8";
        return true;
    }
}

// בדיקת שם משתמש
function checkUserName(userName) {
    var indexOfSpace = userName.indexOf(" ");
    var containNumber = false; // משתנה בוליאני שבודק אם יש מספרים בשם משתמש
    var containLetter = false; // משתנה בוליאני שבודק אם יש אותיות בשם משתמש
    var capitalLetter = false; // משתנה בוליאני שבודק האם בשם המשתמש יש אותיות גדולות
    var firstDigit = userName[0]; // הסיפרה הראשונה 
    var wrongChar = "/#!£$%^&*(){}'?><:;+,-=[]"; // תווים אסורים               

    document.getElementById("error_username").innerHTML = indexOfSpace;


    // בדיקה האם המשתמש הכניס את שם המשתמש
    if (userName.length == 0) {
        document.getElementById("error_username").innerHTML = "You must fill out this field";
        return false;
    }


    // אסור שהסיפרה הראשונה תהיה מספר
    if (firstDigit >= 0 && firstDigit <= 9) {
        document.getElementById("error_username").innerHTML = "User name can not start with a digit";
        return false;
    }

    // בדיקה האם יש רווח במחרוזת
    if (indexOfSpace != -1) // יש רווח במחרוזת 
    {
        document.getElementById("error_username").innerHTML = "User name can not contain space";
        return false;
    }

    // בדיקה האם השם משתמש קצר מדי - מתחת ל-5 תווים
    if (userName.length < 5) {
        document.getElementById("error_username").innerHTML = "User name must contain more than 4 characters";
        return false;
    }

    // בדיקה האם יש גם אותיות וגם מספרים בשם משתמש ואין אותיות גדולות
    for (var i = 0; i < userName.length; i++) {
        if (userName[i] >= 0 && userName[i] <= 9) {
            containNumber = true;
        }
        if (userName[i] >= 'a' && userName[i] <= 'z') {
            containLetter = true;
        }
        if (userName[i] >= 'A' && userName[i] <= 'Z') {
            capitalLetter = true;
        }
        // אם נמצא תו שאסור שיהיה באימייל
        if (wrongChar.includes(userName[i])) {
            document.getElementById("error_username").innerHTML = "User name can not include " + wrongChar;
            return false;
        }
    }
    if (capitalLetter == true) {
        document.getElementById("error_username").innerHTML = "User name can not contain capital letters";
        return false;
    }
    if (containNumber == false) {
        document.getElementById("error_username").innerHTML = "User name must contain numbers";
        return false;
    }
    if (containLetter == false) {
        document.getElementById("error_username").innerHTML = "User name must contain letters";
        return false;
    }

    document.getElementById("error_username").innerHTML = "";
    return true;
}

// בדיקת סיסמה
function checkPassword(password, MediumPassword, StrongPassword) {

    var strongChar = "!@£$%^&*()_+=-~[]{}'?/<>;";

    // אם המשתמש לא הכניס סיסמה
    if (password.length == 0) {
        document.getElementById("error_password").innerHTML = "You must fill out this field";
        document.getElementById("MediumPassword").innerHTML = "";
        document.getElementById("StrongPassword").innerHTML = "";
        return false;
    }

    // סיסמה חלשה
    if (password.length <= 5) {
        document.getElementById("error_password").innerHTML = "Weak Password";
        document.getElementById("MediumPassword").innerHTML = "";
        document.getElementById("StrongPassword").innerHTML = "";
        return false;
    }


    // סיסמה בינונית וחזקה
    for (var i = 0; i < password.length; i++) {
        if (strongChar.includes(password[i]) && password.length >= 10) {
            document.getElementById("StrongPassword").innerHTML = "Strong Password";
            document.getElementById("error_password").innerHTML = "";
            document.getElementById("MediumPassword").innerHTML = "";
            return true;
        }
        else if (password.length <= 9) {
            document.getElementById("MediumPassword").innerHTML = "Medium Password - Password must contain one of these: !@£$%^&*()_+=-~[]{}'?/<>; and at least 10 characters";
            document.getElementById("error_password").innerHTML = "";
            document.getElementById("StrongPassword").innerHTML = "";
            return false;
        }
    }
}

// בדיקת אימות סיסמה
function checkConfirmPassword(confirmPassword) {
    var password = document.forms["registration_form"]["Password"].value; // סיסמה

    // אם השתמש לא הכניס אימות סיסמה
    if (confirmPassword.length == 0) {
        document.getElementById("error_confirm_password").innerHTML = "You must fill out this field";
        return false;
    }

    // אם האימות סיסמה לא זהה לסיסמה
    else if (password != confirmPassword) {
        document.getElementById("error_confirm_password").innerHTML = "The passwords do not match";
        return false;
    }
    document.getElementById("error_confirm_password").innerHTML = "";
    return true;
}

// בדיקת אימייל
function checkEmail(email) {
    var afterShtrudel = "";  // מה שכתוב אחרי השטרודל
    var beforeShtrudel = ""; // מה שכתוב לפני השטרודל
    var shtrudelLocation = email.indexOf('@');   // @ - מיקום ה
    var numberOfPoints = 0; // משתנה מסוג מונה שבודק כמה נקודות [.] יש באימייל
    var numberOfShtrudels = 0; // משתנה מסוג מונה שבודק כמה @ יש באימייל
    var pointLocation; // מיקום הנקודה אחרי השטרודל
    var indexOfSpace = email.indexOf(" ");
    var wrongChar = "/#!£$%^&*(){}'?><,:;+-=[]"; // תווים אסורים               
    var textBetweenShtrudelToPoint = ""; // מה שכתוב בין השטרודל לנקודה
    var textAfterPoint = ""; // מה שכתוב אחרי הנקודה


    // בדיקה האם המשתמש הכניס אימייל
    if (email.length == 0) {
        document.getElementById("error_mail").innerHTML = "You must fill out this field";
        return false;
    }


    // בדיקה האם יש רווח במחרוזת
    if (indexOfSpace != -1) // יש רווח במחרוזת 
    {
        document.getElementById("error_mail").innerHTML = "Email can not contain space";
        return false;
    }

    // בדיקה האם נמצא שטרודל באימייל ואם יש יותר משטרודל אחד
    for (var j = 0; j < email.length; j++) {
        if (email[j] == "@") {
            numberOfShtrudels++;
        }
        // אם נמצא תו שאסור שיהיה באימייל
        if (wrongChar.includes(email[j])) {
            document.getElementById("error_mail").innerHTML = "Email can not include " + wrongChar;
            return false;
        }
    }
    // אם לא נמצא סימן השטרודל
    if (numberOfShtrudels == 0) {
        document.getElementById("error_mail").innerHTML = "Email must contain [@]";
        return false;
    }
    // אם יש יותר מסימן שטרודל אחד
    else if (numberOfShtrudels > 1) {
        document.getElementById("error_mail").innerHTML = "Email can not contain more than one [@]";
        return false;
    }


    // מציאת הטקסט לפני השטרודל
    for (var k = 0; k < shtrudelLocation; k++) {
        beforeShtrudel += email[k];
    }
    // בדיקה האם יש טקסט לפני השטרודל
    if (beforeShtrudel == "") {
        document.getElementById("error_mail").innerHTML = "Email must contain text before the [@]";
        return false;
    }
    // בדיקת אורך הטקסט לפני השטרודל
    else if (beforeShtrudel.length <= 5) {
        document.getElementById("error_mail").innerHTML = "Email must contain more than 5 characters before the [@]";
        return false;
    }

    // מציאת הכתוב מהשטרודל עד הסוף
    for (var i = shtrudelLocation + 1; i < email.length; i++) {
        afterShtrudel += email[i];
    }

    // מציאת כמות הנקודות מאחרי ה@ עד סוף המחרוזת
    for (var n = shtrudelLocation + 1; n < email.length; n++) {
        if (email[n] == '.') {
            numberOfPoints++;
            pointLocation = n;
        }
    }

    // אם אין כתוב בין השטרודל לנקודה
    if (email[shtrudelLocation + 1] == '.') {
        document.getElementById("error_mail").innerHTML = "Email must contain text between [@] and [.]";
        return false;
    }

    // האם יש נקודה אחרי השטרודל
    if (numberOfPoints == 0) {
        document.getElementById("error_mail").innerHTML = "Email must contain [.] after the [@]";
        return false
    }

    // בדיקה אם יש יותר מנקודה אחת אחרי השטרודל
    if (numberOfPoints > 1) {
        document.getElementById("error_mail").innerHTML = "Email can not contain more than one [.] after [@]";
        return false;
    }

    // (אם לא כתוב כלום אחרי הנקודה (שאחרי השטרודל
    if (email[pointLocation + 1] == null) {
        document.getElementById("error_mail").innerHTML = "Email must contain text after the [.]";
        return false;
    }


    // מציאת הטקסט בין השטרודל לנקודה
    for (var a = shtrudelLocation + 1; a < pointLocation; a++) {
        textBetweenShtrudelToPoint += email[a];
    }
    // בדיקה האם יש מינימום תווים בין השטרודל לנקודה
    if (textBetweenShtrudelToPoint.length <= 4) {
        document.getElementById("error_mail").innerHTML = "Email must contain more than 4 characters between [@] to [.]";
        return false;
    }

    // מציאת הטקסט אחרי הנקודה
    for (var b = pointLocation + 1; b < email.length; b++) {
        textAfterPoint += email[b];
    }
    // בדיקה האם יש מינימום תווים אחרי הנקודה
    if (textAfterPoint.length <= 2) {
        document.getElementById("error_mail").innerHTML = "Email must contain more than 2 characters after [.]";
        return false;
    }

    document.getElementById("error_mail").innerHTML = "";
    return true;

}

// בדיקת האם רובוט
function checkRobot(response) {

    // בדיקה האם המשתמש סימן את בדיקת הרובוט
    if (response.length == 0) {
        document.getElementById("error_robot").innerHTML = "You must fill out this field";
        return false;
    }
    else {
        document.getElementById("error_robot").innerHTML = "";
        return true;
    }
}

// בדיקת מגדר מסוג רדיו
function checkRadio(gender) {

    if ((gender[0].checked) || (gender[1].checked) || (gender[2].checked)) {
        document.getElementById("error_gender").innerHTML = "";
        return true;
    }

    else {
        document.getElementById("error_gender").innerHTML = "You must fill out this field";
        return false;
    }
    return true;
    document.getElementById("error_gender").innerHTML = "";
}

// בדיקת מדינה 
function checkCountry(country) {
    if (country == "select") {
        document.getElementById("error_country").innerHTML = "You must fill out this field";
        return false;
    }
    else {
        document.getElementById("error_country").innerHTML = "";
        return true;
    }
}

// בדיקת גיל
function checkAge(age) {
    if (age.length == 0) {
        document.getElementById("error_age").innerHTML = "You must fill out this field";
        return false;
    }
    if (age <= 0) {
        document.getElementById("error_age").innerHTML = "Age can not be a negative number";
        return false;
    }

    if (age <= 0 || age > 120) {
        document.getElementById("error_age").innerHTML = "You entered an unreasonable age";
        return false;
    }

    if (age < 7) {
        document.getElementById("error_age").innerHTML = "People under 7 are not allowed to use the site";
        return false;
    }
    else {
        document.getElementById("error_age").innerHTML = "";
        return true;
    }
}

// בדיקת תאריך לידה
function checkDateBirth(date) {
    var firstHyphen = date.indexOf('-'); // מיקום המכף הראשון
    var year = "";


    if (date.length == 0) {
        document.getElementById("error_date_of_birth").innerHTML = "You must fill out this field";
        return false;
    }

    // בדיקת שנת הלידה - מה שכתוב לפני המכף הראשון
    for (var i = 0; i < firstHyphen; i++) {
        year += date[i];
    }

    // אם שנת הלידה 
    if (year < 1900 || year > 2020) {
        document.getElementById("error_date_of_birth").innerHTML = "You entered an unreasonable year";
        return false;
    }

    if (date.length == 0) {
        document.getElementById("error_date_of_birth").innerHTML = "You must fill out this field";
        return false;
    }

    document.getElementById("error_date_of_birth").innerHTML = "";
    return true;
}