var copyBtn = document.getElementById('copy_emails_btn')
console.log(copyBtn)

var all_emails = ''

copyBtn.addEventListener('click', () => {
    console.log('click')
    var emails_data = document.getElementById('id_contacts-0-email').childNodes
    for (var email_data of emails_data) {
        if (email_data.nodeName === 'OPTION' && email_data.hasAttribute('selected')){
            all_emails += email_data.textContent + '\n'
        }
        }
    console.log(all_emails)
    navigator.clipboard.writeText(all_emails)
    all_emails = ''
})
