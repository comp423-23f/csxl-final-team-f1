# Overview:

The XL has equipment, and will be getting more, that it would like to open up for students to reserve for varying lengths of time during the week or over the weekend.

# Key Personas:

The key personas of the equipment reservation system will be Student, Ambassador, and Admin.

The Student needs an easy-to-understand interface that will allow them to navigate to an equipment reservation page. They also need to be able to see which equipment is available and which is not, be able to sign a liability waiver the first time they reserve equipment, and confirm a request to reserve equipment so that an Ambassador can finalize the process.

The Ambassador needs an interface to confirm reservation requests, confirm student liability forms, and finalize reservation requests for Students so that they can retrieve the equipment for the Student to borrow. They also need an interface to check equipment back into the list of available equipment.

The Admin needs an interface to add new equipment to the list of reservable equipment. In the case that a piece of equipment needs repair/is broken, the Admin will also need a way to remove equipment from the list of reservable equipment in that interface.

#Stories

Stories 1, 2 and 3 are tied for most importance, 4 and 5 are second most important, and 6 is least important that is still necessary for minimum viability. Story 7 is not necessary but would be good to complete if there is time.
Story 1: As Silas Student, I would like to see a list of available equipment during the period that I want to check something out, so that I can make a decision on what to check out.
Story 2: As Silas Student, I would like to request a checkout so that I can go in-person to pick it up.
Story 3: As Abraham Ambassador, I would like to complete a checkout when given a pid, so that students can actually check out the equipment they requested.
Story 4: As Abraham Ambassador, I would like to check a piece of equipment back in using a student's pid, so that someone else can check it out.
Story 5: As Alan Admin, I would like to add new pieces of equipment to the list of available equipment so that students have more options of what to check out.
Story 6: As Silas Student, I would like to sign a usage and liability agreement before my first checkout so that there is proof that I know what the consequences are if I break or lose the equipment.
Story 7: As Abraham Ambassador, I would like to send notifications for equipment that is due in 1 day, 0 days, or overdue so that it can be returned promptly for other students to use.
(Optional Story 8): As Leonardo CAD Leader, I would like to have the functionalities of stories 1, 2, and 6 for organizations so that I can check out enough equipment for my club to use at a meeting/workshop/whatever.

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
