from flask import url_for
from .base import BaseTest

class PortfolioTest(BaseTest):
    def test_view_home(self):
        '''Тестує, чи головна сторінка завантажується коректно.'''
        with self.client:
            response = self.client.get(url_for('portfolio.home'))

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome to INVISIBLE WEBSITE', response.data)
            self.assertIn(b'Viktor Prystai Website', response.data)

    def test_view_portfolio(self):
        '''Тестує, чи сторінка портфоліо завантажується коректно.'''
        with self.client:
            response = self.client.get(url_for('portfolio.about'))

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Few Words About Me', response.data)

    def test_view_skills(self):
        '''Тестує, чи сторінка навичок завантажується коректно.'''
        with self.client:
            response = self.client.get(url_for('portfolio.skill'))

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'MY SKILLS page', response.data)
            self.assertIn(b'CSS and HTML', response.data)
            self.assertIn(b'C# .NET', response.data)
            self.assertIn(b'Angular and js', response.data)

