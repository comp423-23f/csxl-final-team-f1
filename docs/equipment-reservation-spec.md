# Descriptions and sample data representations of new/modified model representation(s) and API routes

**Equipment Model:**

    id: int | None = None

    name: str

    reservable: bool

    image: str

Ex -

    id: 1

    name: Keyboard

    reservable: True

    image: keyboard.jpg

The equipment model stores information needed to identify equipment and whether it is reserved or not by users

API Route - `@api.put("", responses={404: {"model": None}}, response_model=Equipment, tags=["Equipment"])`

**Updated User Model:**

    signed_agreement: bool

Ex -

    signed_agreement: True

The signed_agreement field tracks whether users have signed the liability agreement or not

API Route - `@api.put("", response_model=UserDetails, tags=["Profile"])`

# Description of underlying database/entity-level representation decisions

We created the `equipment_entity` and updated the "`Profile`" interface defined in `profile.service.ts`.

For the equipment, we needed to create a new model and entity to store and access data related to equipment. However, to track whether user's signed the agreement form, we could simply add a field to the existing profile and user models.

# Design choice weighed with the trade-offs and justification for the decision

We decided to display all equipment on the page rather than just the ones that are available. This allows the end-user to see how many of each equipment are available and their current status. It also gives them the ability to specifically reserve the piece of equipment (Ex. Keyboard 2). In the future, we expect the equipment to have further detail associated with them, like "Razer" Keyboard, "Logitech" Keyboard, etc. Thus, by showing all equipment, we are giving them the ability to choose a specific piece of equipment.

# Development concerns: Brief guide of the files and concerns they need to understand to get up-to-speed

Equipment on `equipment-page.component.html` is displayed by storing equipment from the database in an observable list of equipment in `equipment-page.component.ts`. Then, a equipment card widget is created for each equipment and styled according to the status of the `reservable` field.

When a user clicks "Reserve" on a piece of equipment, a conditional check is performed on the user's `signed_agreement` field (under development as of 11/19). If `signed_agreement` is `False`, the user will be taken to the profile page where they must sign the liability agreement to set the field to `True` before proceeding to reserve the equipment again. The `signed_agreement` field is updated through the `update_profile()` API call, and changes the `signed_agreement` field to `True` in the `ProfileEditorComponent`'s `agreeToTerms()` function.
