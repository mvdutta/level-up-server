"""Module for generating events by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all events 
            db_cursor.execute("""
                SELECT
                    e.id,
                    e.description,
                    e.game_id,
                    e.organizer_id,
                    e.event_time,
                    e.event_date,
                    g.game_title AS game_name,
                    u.first_name || " " || u.last_name AS full_name
                FROM levelupapi_event e
                JOIN levelupapi_game g ON g.id = e.game_id
                JOIN levelupapi_gamer gm ON gm.id = e.organizer_id
                JOIN auth_user u ON gm.user_id = u.id   
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each event.
            # This will be the structure of the events_by_user list:
            # [
            #     {
            #         "gamer_id": 1,
            #         "full_name": "Molly Ringwald",
            #         "events": [
            #             {
            #                 "id": 5,
            #                 "date": "2020-12-23",
            #                 "time": "19:00",
            #                 "game_name": "Fortress America"
            #             }
            #         ]
            #     }
            # ]
          
            events_by_user = []

            for row in dataset:
                # TODO: Create a dictionary called event 
                event = {
                    'id': row['id'],
                    'description': row['description'],
                    'game_name': row['game_name'],
                    'event_date': row['event_date'],
                    'event_time': row['event_time']
                }

                # See if the event has been added to the events_by_user list already
                user_dict = None
                for user_event in events_by_user:
                    if user_event['organizer_id'] == row['organizer_id']:
                        user_dict = user_event

                if user_dict:
                    # If the user_dict is already in the events_by_user list, append the event to the events list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the events_by_user list, create and add the user to the list
                    events_by_user.append({
                        "organizer_id": row['organizer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                    })

        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
