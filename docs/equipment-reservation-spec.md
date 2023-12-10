# Descriptions and sample data representations of new/modified model representation(s) and API routes

**Equipment Model:**
id: int

name: str

reservable: bool

is_keyboard: bool

is_mouse: bool

is_vr: bool

Ex -

id: 1

name: Keyboard

reservable: True

is_keyboard: True

is_mouse: False

is_vr: False

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

We chose to go with a similar layout to "coworking" to ensure the entire website's design is consistent. This makes the feature easy to understand for the user. Additionally, the liability form is attached to the profile since it functions in a similar way to the other profile fields.

# Development concerns: Brief guide of the files and concerns they need to understand to get up-to-speed

The amount of each equipment is displayed on the `equipment-home.component.html` page by calling the `dropin-availability-card.widget.html` widget. The widget displays the amount available of each equipment by checking the length of the `equipment_available_now[]` array for each equipment in the `EquipmentCategory[]` array.

When a user clicks "Confirm in X minutes" on a type of equipment, a conditional check is performed on the user's `signed_agreement` field. If `signed_agreement` is `False`, the user will be taken to the profile page where they must sign the liability agreement to set the field to `True` before proceeding to reserve the equipment again. The `signed_agreement` field is updated through the `update_profile()` API call, and changes the `signed_agreement` field to `True` in the `ProfileEditorComponent`'s `agreeToTerms()` function.
