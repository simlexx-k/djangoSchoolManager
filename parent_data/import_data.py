from learners.models import LearnerRegister
from parent_data.models import TempParent, TempParentLearnerRelationship, Parent, ParentLearnerRelationship

def import_parent_data():
    # Import TempParent data into Parent
    for temp_parent in TempParent.objects.all():
        parent = Parent.objects.create(
            first_name=temp_parent.first_name,
            last_name=temp_parent.last_name,
            email=temp_parent.email,
            phone_number=temp_parent.phone_number,
            address=temp_parent.address,
            occupation=temp_parent.occupation,
            relationship_to_learner=temp_parent.relationship_to_learner,
        )
        print(f"Imported parent: {parent}")

    # Import TempParentLearnerRelationship data into ParentLearnerRelationship
    for temp_relationship in TempParentLearnerRelationship.objects.all():
        try:
            learner = LearnerRegister.objects.get(id=temp_relationship.learner_id)
            parent = Parent.objects.get(email=TempParent.objects.get(id=temp_relationship.parent_id).email)
            relationship = ParentLearnerRelationship.objects.create(
                parent=parent,
                learner=learner,
                is_primary_contact=temp_relationship.is_primary_contact,
            )
            print(f"Imported relationship: {relationship}")
        except LearnerRegister.DoesNotExist:
            print(f"Learner with ID {temp_relationship.learner_id} does not exist.")
        except Parent.DoesNotExist:
            print(f"Parent with ID {temp_relationship.parent_id} does not exist.")

if __name__ == "__main__":
    import_parent_data()