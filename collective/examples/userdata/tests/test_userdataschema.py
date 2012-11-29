import transaction

from plone.app.testing import TEST_USER_ID, setRoles

from ..testing import FunctionalTestCase

class TestUserDataSchema(FunctionalTestCase):
    def test_personalinformationextended(self):
        """Ensure the fields we wanted were added to @@personal-information
           and @@user-information forms
        """
        setRoles(self.layer['portal'], TEST_USER_ID, ['Manager'])
        transaction.commit()
        for url in ['/@@personal-information', '/@@user-information']:
            browser = self.getBrowser(url)
            control = browser.getControl(name='form.widgets.gender')
            self.assertEquals(
                browser.getControl(name='form.widgets.firstname').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.widgets.lastname').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.widgets.gender').type,
                'radio') # Using custom widget
            self.assertEquals(
                browser.getControl(name='form.widgets.birthdate-day').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.widgets.birthdate-month').type,
                'select')
            self.assertEquals(
                browser.getControl(name='form.widgets.birthdate-year').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.widgets.city').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.widgets.country').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.widgets.phone').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.widgets.newsletter:list').type,
                'checkbox')
            # We hid accept, so shouldn't be here
            with self.assertRaisesRegexp(LookupError,'form.accept:list'):
                browser.getControl(name='form.accept:list')

    def test_registerextended(self):
        """Ensure the fields we wanted were added to @@register and @@add-user
           forms
        """
        portal = self.layer['portal']
        portal.MailHost.smtp_host = 'localhost'
        setattr(portal, 'email_from_address', 'admin@example.com')
        setRoles(self.layer['portal'], TEST_USER_ID, ['Manager'])
        transaction.commit()
        for url in ['/@@register', '/@@new-user']:
            browser = self.getBrowser(url)
            control = browser.getControl(name='form.gender')
            self.assertEquals(
                browser.getControl(name='form.firstname').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.lastname').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.gender').type,
                'radio') # Using custom widget
            self.assertEquals(
                browser.getControl(name='form.birthdate-day').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.birthdate-month').type,
                'select')
            self.assertEquals(
                browser.getControl(name='form.birthdate-year').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.city').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.country').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.phone').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.newsletter:list').type,
                'checkbox')
            if url == '/@@register':
                self.assertEquals(
                    browser.getControl(name='form.accept:list').type,
                    'checkbox')
            else:
                # We hid accept, so shouldn't be here
                with self.assertRaisesRegexp(LookupError,'form.accept:list'):
                    browser.getControl(name='form.accept:list')

    def test_validateaccept(self):
        """Make sure we have to check the 'accept' box
        """
        # Allow users to set their own passwords when registering
        setRoles(self.layer['portal'], TEST_USER_ID, ['Manager'])
        transaction.commit()
        browser = self.getBrowser('/@@security-controlpanel')
        browser.getControl('Enable self-registration').selected = True
        browser.getControl('Let users select their own passwords').selected = True
        browser.getControl('Save').click()
        self.assertTrue('Changes saved' in browser.contents)

        # Try registering without clicking "accept"
        browser = self.getBrowser('/@@register')
        browser.getControl('User Name').value = 'mrcamel'
        browser.getControl('E-mail').value = 'camel@example.com'
        browser.getControl('Password').value = 'dr0medary'
        browser.getControl('Confirm password').value = 'dr0medary'
        browser.getControl(name='form.gender').value = ['Male']
        browser.getControl('Register').click()
        # Should still be on the form at this point, check the box
        self.assertTrue('@@register' in browser.url)
        browser.getControl('Password').value = 'dr0medary'
        browser.getControl('Confirm password').value = 'dr0medary'
        browser.getControl(name='form.accept:list').value = True
        browser.getControl('Register').click()
        self.assertTrue('You have been registered' in browser.contents)

    def test_setvalues(self):
        """Make sure we can set and retrieve all values
        """
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        transaction.commit()
        browser = self.getBrowser('/@@personal-information')
        browser.getControl('E-mail').value = 'beth@example.com'
        browser.getControl(name='form.widgets.firstname').value = 'Beth'
        browser.getControl(name='form.widgets.lastname').value = 'Orton'
        browser.getControl(name='form.widgets.gender').value = ['Female']
        browser.getControl(name='form.widgets.birthdate-day').value = '15'
        browser.getControl(name='form.widgets.birthdate-month').value = ['3']
        browser.getControl(name='form.widgets.birthdate-year').value = '1980'
        browser.getControl(name='form.widgets.city').value = 'Norwich'
        browser.getControl(name='form.widgets.country').value = 'UK'
        browser.getControl(name='form.widgets.phone').value = '012345'
        browser.getControl(name='form.widgets.newsletter:list').value = ['selected']
        browser.getControl('Save').click()
        self.assertTrue('Changes saved.' in browser.contents)

        # Should be able to retrieve values when page is reloaded
        browser.open(portal.absolute_url() + '/@@personal-information')
        self.assertEquals(
            browser.getControl('E-mail').value,
            'beth@example.com')
        self.assertEquals(
            browser.getControl(name='form.widgets.firstname').value,
            'Beth')
        self.assertEquals(
            browser.getControl(name='form.widgets.lastname').value,
            'Orton')
        self.assertEquals(
            browser.getControl(name='form.widgets.gender').value,
            ['Female'])
        self.assertEquals(
            browser.getControl(name='form.widgets.birthdate-day').value,
            '15')
        self.assertEquals(
            browser.getControl(name='form.widgets.birthdate-month').value,
            ['3'])
        self.assertEquals(
            browser.getControl(name='form.widgets.birthdate-year').value,
            '1980')
        self.assertEquals(
            browser.getControl(name='form.widgets.city').value,
            'Norwich')
        self.assertEquals(
            browser.getControl(name='form.widgets.country').value,
            'UK')
        self.assertEquals(
            browser.getControl(name='form.widgets.phone').value,
            '012345')
        self.assertEquals(
            browser.getControl(name='form.widgets.newsletter:list').value,
            ['selected'])
