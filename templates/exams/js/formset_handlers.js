document.addEventListener('DOMContentLoaded', function() {
    const addFormBtns = document.querySelectorAll('.add-form-btn');
    
    addFormBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const formset = this.closest('.formset');
            const formCount = formset.querySelector('[name$=TOTAL_FORMS]');
            const formNum = parseInt(formCount.value);
            const newForm = formset.querySelector('.formset-form').cloneNode(true);
            
            newForm.innerHTML = newForm.innerHTML.replace(/-\d+-/g, `-${formNum}-`);
            
            // Set learner and exam_type values
            const learnerSelect = document.getElementById('id_learner');
            const examTypeSelect = document.getElementById('id_exam_type');
            const learnerInput = newForm.querySelector('input[name$="-learner"]');
            const examTypeInput = newForm.querySelector('input[name$="-exam_type"]');
            
            if (learnerInput) learnerInput.value = learnerSelect.value;
            if (examTypeInput) examTypeInput.value = examTypeSelect.value;
            
            formset.insertBefore(newForm, this);
            formCount.value = formNum + 1;
        });
    });
});