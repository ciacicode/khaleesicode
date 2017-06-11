__author__= 'ciacicode'
from flask_wtf import Form
from mysite.configs.khal_config import Config
from wtforms import SubmitField, TextAreaField
from watson_developer_cloud import PersonalityInsightsV3
import json
import pdb


#class for Profile input form
class Profile(Form):
    profile = TextAreaField('profile')
    submit = SubmitField('Calculate')


def get_personality_insights(profile):
    """
    profile: text input
    insights: json output
    """
    personality_insights = PersonalityInsightsV3(
        version='2016-10-20',
        username=Config.WATSON['username'],
        password=Config.WATSON['password'])
    personality = personality_insights.profile(profile,
                                               content_type='text/plain;charset=utf-8',
                                               raw_scores=True, consumption_preferences=True)
    pdb.set_trace()
    #serialise to string
    result = json.loads(json.dumps(personality))
    return result

def generate_chart_data():
    """
    personality_insights: as json from watson
    returns data: ready for chart display
    """
    pass
