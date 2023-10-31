# Technical Implementation Opportunities and Planning

1. **Files we will depend on**
   `backend/models/user.py`
   `backend/services/coworking/permission.py`

   **Files we will extend**
   `backend/models/coworking/reservation.py`
   `backend/models/user.py`
   `backend/api/coworking/ambassador.py`
   `backend/services/coworking/reservation.py`
   `frontend/src/app/navigation/navigation.component.html`

   **Files we will interact with**
   `backend/services/coworking/role.py`
   `backend/api/admin/roles.py`

2. We will modify the organization card widgets to display equipment so that we can reuse the widgets to display equipment.
3. We will need to create an equipment model, time range model, availability model, and status model so that we can use these objects to properly reserve equipment.
4. We will need to add a route to the equipment availability page, equipment reservation page. We will also need to add routes to get user data through `profile.service.ts`.
5. The privacy concerns revolve around the user's reserved equipment data and liability form data. When a user checks out a piece of equipment, only the user themselves, the ambassadors, and the admin should be able to see their checked out equipment. Only ambassadors and the admin should be able to check items back in. These concerns will allow us to properly compartmentalize data and keep the reservation system private/secure.
