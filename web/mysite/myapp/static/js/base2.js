const language = {
    eng: {
        footer: {
            aboutUs: "About Us",
            aboutUsDescription: "We are dedicated to providing the best service possible.",
            ourStory: "Our Story",
            ourTeam: "Our Team",
            careers: "Careers",
            help: "Help",
            needAssistance: "Need assistance? We're here to help.",
            faqs: "FAQs",
            supportCenter: "Support Center",
            contactSupport: "Contact Support",
            contact: "Contact",
            haveQuestions: "Have questions? Reach out to us.",
            emailUs: "Email Us",
            findUs: "Find Us",
            feedback: "Feedback",
            privacyPolicy: "Privacy Policy",
            termsOfService: "Terms of Service",
        },
        currentLanguage: {
            about: "About us",
            help: "Help",
            contact: "Contact",
            services: "Services",
        },
        header: {
            title: "Welcome to Our Platform",
            subtitle: "Your place for sharing and exchanging",
        },
        home: { // New section for home page
            welcomePart1: "Welcome",
            welcomePart2: "to",
            greetingText: "Do you want to donate or receive items but have no way? Use the Dorm Exchange platform to share unwanted items with friends in the same dorm or other dorms easily. Whether it's books, clothes, or electronics, all for free. Help reduce waste and create happiness for those who want to give and receive conveniently, quickly, and safely.",
            registerButton: "Sign Up Now",
            loginButton: "I Already Have an Account",
        }
    },
    th: {
        footer: {
            aboutUs: "เกี่ยวกับเรา",
            aboutUsDescription: "เรามุ่งมั่นที่จะให้บริการที่ดีที่สุดแก่คุณ",
            ourStory: "เรื่องราวของเรา",
            ourTeam: "ทีมงานของเรา",
            careers: "อาชีพ",
            help: "ช่วยเหลือ",
            needAssistance: "ต้องการความช่วยเหลือ? เรายินดีที่จะช่วยคุณ",
            faqs: "คำถามที่พบบ่อย",
            supportCenter: "ศูนย์ช่วยเหลือ",
            contactSupport: "ติดต่อฝ่ายสนับสนุน",
            contact: "ติดต่อ",
            haveQuestions: "มีคำถาม? ติดต่อเราได้เลย",
            emailUs: "ส่งอีเมลถึงเรา",
            findUs: "ค้นหาเรา",
            feedback: "ข้อเสนอแนะ",
            privacyPolicy: "นโยบายความเป็นส่วนตัว",
            termsOfService: "ข้อกำหนดในการให้บริการ",
        },
        currentLanguage: {
            about: "เกี่ยวกับเรา",
            help: "ช่วยเหลือ",
            contact: "ติดต่อ",
            services: "บริการ",
        },
        header: {
            title: "ยินดีต้อนรับสู่แพลตฟอร์มของเรา",
            subtitle: "สถานที่ของคุณสำหรับการแบ่งปันและแลกเปลี่ยน",
        },
        home: { // New section for home page
            welcomePart1: "ยินดีต้อน",
            welcomePart2: "รับสู่",
            greetingText: "คุณต้องการบริจาคสิ่งของหรือรับสิ่งของ แต่ยังไม่มีช่องทาง? ใช้แพลตฟอร์ม Dorm Exchange สิ ร่วมแบ่งปันสิ่งของที่ไม่ใช้แล้วให้กับเพื่อนๆ ในหอพักเดียวกันหรือหอพักอื่นได้ง่ายๆ ไม่ว่าจะเป็นหนังสือ เสื้อผ้า หรือเครื่องใช้ไฟฟ้า ทั้งหมดนี้ฟรีไม่มีค่าใช้จ่าย ช่วยลดการสูญเปล่าและสร้างความสุขให้กับคนที่ต้องการ รับ-ให้ได้อย่างสะดวก รวดเร็ว และปลอดภัย",
            registerButton: "สมัครใช้งานเลย",
            loginButton: "ฉันมีบัญชีอยู่เเล้ว",
        }
    }
};


// Set the default language to Thai
let currentLanguage = 'th';

// Update language immediately on page load
changeLanguage(currentLanguage);

function toggleLanguage() {
    const switchElement = document.getElementById('languageSwitch');
    currentLanguage = switchElement.checked ? 'th' : 'eng';
    changeLanguage(currentLanguage);
}

function changeLanguage(lang) {
    // Update footer section
    const footerItems = {
        aboutUs: 'footerAboutUs',
        aboutUsDescription: 'footerAboutUsDescription',
        ourStory: 'aboutUsLink',
        ourTeam: 'teamLink',
        careers: 'careersLink',
        help: 'footerHelp',
        needAssistance: 'footerNeedAssistance',
        faqs: 'faqsLink',
        supportCenter: 'supportCenterLink',
        contactSupport: 'contactSupportLink',
        contact: 'footerContact',
        haveQuestions: 'footerHaveQuestions',
        emailUs: 'emailUsLink',
        findUs: 'findUsLink',
        feedback: 'feedbackLink',
        privacyPolicy: 'privacyPolicyLink',
        termsOfService: 'termsOfServiceLink'
    };
    
    const navbarItems = {
        about: 'aboutUsNav',
        help: 'helpNav',
        contact: 'contactNav',
        services: 'servicesNav'
    };

    // New section for header
    const headerItems = {
        title: 'headerTitle',
        subtitle: 'headerSubtitle'
    };

    // New section for home
    const homeItems = {
        welcomePart1: 'welcomePart1',
        welcomePart2: 'welcomePart2',
        greetingText: 'greetingText',
        registerButton: 'registerButton',
        loginButton: 'loginButton',
    };

    // Update all text elements
    for (const key in footerItems) {
        document.getElementById(footerItems[key]).innerText = language[lang].footer[key];
    }
    
    for (const key in navbarItems) {
        document.getElementById(navbarItems[key]).innerText = language[lang].currentLanguage[key];
    }

    // Update header elements
    for (const key in headerItems) {
        document.getElementById(headerItems[key]).innerText = language[lang].header[key];
    }

    // Update home elements
    for (const key in homeItems) {
        document.getElementById(homeItems[key]).innerText = language[lang].home[key];
    }
}

