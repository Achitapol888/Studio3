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
            contact: "ติดต่อ"
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
    
    // Update content dynamically
    Object.keys(footerItems).forEach(key => {
        const element = document.getElementById(footerItems[key]);
        if (element) {
            element.textContent = language[lang].footer[key];
        }
    });
    
    Object.keys(navbarItems).forEach(key => {
        const element = document.getElementById(navbarItems[key]);
        if (element) {
            element.textContent = language[lang].currentLanguage[key];
        }
    });
}
