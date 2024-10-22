<template>
  <div class="grades p-4 sm:p-6 md:p-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-800">My Academic Performance</h1>
      <button @click="exportToPDF" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
        </svg>
        Export to PDF
      </button>
    </div>
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
    </div>
    <div v-else-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
      <p class="font-bold">Error</p>
      <p>{{ error }}</p>
    </div>
    <div v-else class="space-y-4">
      <div v-for="(examResult, index) in examResults" :key="examResult.exam_type" class="bg-white shadow-md rounded-lg overflow-hidden">
        <div 
          @click="toggleExam(index)" 
          class="bg-gray-100 px-6 py-4 cursor-pointer flex justify-between items-center"
        >
          <div>
            <h2 class="text-xl font-semibold text-gray-800">{{ examResult.exam_type }}</h2>
            <p class="text-sm text-gray-600">{{ formatDate(examResult.date) }}</p>
          </div>
          <svg 
            :class="{'transform rotate-180': expandedExamIndex === index}"
            class="w-6 h-6 transition-transform duration-200" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
        <div v-show="expandedExamIndex === index" class="transition-all duration-300 ease-in-out">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subject</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Grade</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Comment</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="result in examResult.results" :key="result.subject" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ result.subject }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ result.score }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span :class="getGradeColor(result.grade)" class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full">
                      {{ result.grade }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ result.comment }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="bg-gray-50 px-6 py-4">
            <h3 class="text-lg font-semibold text-gray-800 mb-2">Overall Performance</h3>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <p class="text-sm font-medium text-gray-500">Average Score</p>
                <p class="mt-1 text-lg font-semibold text-gray-900">{{ examResult.average_score.toFixed(2) }}</p>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-500">Overall Grade</p>
                <p class="mt-1 text-lg font-semibold" :class="getGradeColor(examResult.overall_grade)">
                  {{ examResult.overall_grade }}
                </p>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-500">Overall Comment</p>
                <p class="mt-1 text-sm text-gray-700">{{ examResult.overall_comment }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/config'
import jsPDF from 'jspdf'
import 'jspdf-autotable'

const examResults = ref([])
const isLoading = ref(true)
const error = ref(null)
const expandedExamIndex = ref(null)
const schoolInfo = ref(null)
const learnerInfo = ref(null)

const svgBackground = `
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <defs>
    <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
      <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#E0E0E0" stroke-width="0.5"/>
    </pattern>
  </defs>
  <rect width="100" height="100" fill="url(#grid)" />
</svg>
`;

const fetchGrades = async () => {
  try {
    const response = await api.get('/student/exam-results/')
    examResults.value = response.data
  } catch (err) {
    console.error('Error fetching grades:', err)
    error.value = 'Failed to load grades. Please try again.'
  }
}

const fetchSchoolInfo = async () => {
  try {
    const response = await api.get('/school/info/')
    schoolInfo.value = response.data
  } catch (error) {
    console.error('Error fetching school info:', error)
  }
}

const fetchLearnerInfo = async () => {
  try {
    const response = await api.get('/learner/info/')
    learnerInfo.value = response.data
  } catch (error) {
    console.error('Error fetching learner info:', error)
  }
}

onMounted(async () => {
  isLoading.value = true
  try {
    await Promise.all([fetchGrades(), fetchSchoolInfo(), fetchLearnerInfo()])
  } catch (error) {
    console.error('Error initializing component:', error)
  } finally {
    isLoading.value = false
  }
})

const toggleExam = (index) => {
  if (expandedExamIndex.value === index) {
    expandedExamIndex.value = null // Collapse if clicking on the expanded exam
  } else {
    expandedExamIndex.value = index // Expand the clicked exam
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

const getGradeColor = (grade) => {
  const gradeColors = {
    'EE': 'bg-green-100 text-green-800',
    'ME': 'bg-blue-100 text-blue-800',
    'AE': 'bg-yellow-100 text-yellow-800',
    'BE': 'bg-red-100 text-red-800',
  }
  return gradeColors[grade] || 'bg-gray-100 text-gray-800'
}

const exportToPDF = async () => {
  if (!schoolInfo.value || !learnerInfo.value) {
    await Promise.all([fetchSchoolInfo(), fetchLearnerInfo()]);
  }

  if (!learnerInfo.value) {
    console.error('Learner information not available');
    return;
  }

  const doc = new jsPDF();
  const pageWidth = doc.internal.pageSize.width;
  const pageHeight = doc.internal.pageSize.height;

  // Helper functions
  const addCenteredText = (text, y, size = 12, color = '#000000') => {
    doc.setFontSize(size);
    doc.setTextColor(color);
    const textWidth = doc.getStringUnitWidth(text) * size / doc.internal.scaleFactor;
    doc.text(text, (pageWidth - textWidth) / 2, y);
  };

  const addLine = (y, color = '#000000', width = 0.5) => {
    doc.setDrawColor(color);
    doc.setLineWidth(width);
    doc.line(20, y, pageWidth - 20, y);
  };

  // Cover page
  // School logo
  if (schoolInfo.value.logo_url) {
    const logoImg = new Image();
    logoImg.src = schoolInfo.value.logo_url;
    logoImg.onload = function() {
      doc.addImage(this, 'PNG', (pageWidth - 60) / 2, 20, 60, 60);
    };
  }

  // School name
  doc.setTextColor('#4A90E2');
  doc.setFontSize(24);
  doc.setFont('helvetica', 'bold');
  addCenteredText(schoolInfo.value.name, 100);

  // School address
  doc.setTextColor('#666666');
  doc.setFontSize(12);
  doc.setFont('helvetica', 'normal');
  addCenteredText(schoolInfo.value.address, 110);

  // Decorative line
  addLine(120, '#4A90E2', 1);

  // Report title
  doc.setTextColor('#333333');
  doc.setFontSize(28);
  doc.setFont('helvetica', 'bold');
  addCenteredText('Academic Performance', 140);
  addCenteredText('Report', 155);

  // Academic year
  doc.setTextColor('#4A90E2');
  doc.setFontSize(16);
  addCenteredText(`Academic Year ${new Date().getFullYear()}`, 175);

  // Student name
  doc.setTextColor('#333333');
  doc.setFontSize(20);
  doc.setFont('helvetica', 'bold');
  addCenteredText(learnerInfo.value.name, 210);

  // Student details
  doc.setTextColor('#666666');
  doc.setFontSize(14);
  doc.setFont('helvetica', 'normal');
  addCenteredText(`Grade: ${learnerInfo.value.grade}`, 225);
  addCenteredText(`Student ID: ${learnerInfo.value.learner_id}`, 235);

  // Decorative element
  doc.setDrawColor('#4A90E2');
  doc.setLineWidth(2);
  doc.line(20, pageHeight - 40, pageWidth - 20, pageHeight - 40);

  // Report generation date
  doc.setTextColor('#666666');
  doc.setFontSize(10);
  addCenteredText(`Report generated on ${new Date().toLocaleDateString()}`, pageHeight - 20);

  // Exam Results (subsequent pages)
  examResults.value.forEach((examResult, index) => {
    doc.addPage();
    
    // Header
    doc.setFillColor('#4A90E2');
    doc.rect(0, 0, pageWidth, 30, 'F');
    doc.setTextColor('#FFFFFF');
    doc.setFontSize(18);
    doc.text(examResult.exam_type, 10, 20);
    doc.setFontSize(12);
    doc.text(`Date: ${formatDate(examResult.date)}`, pageWidth - 60, 20);

    // Student info in header
    doc.setTextColor('#000000');
    doc.setFontSize(12);
    doc.text(`${learnerInfo.value.name} - Grade ${learnerInfo.value.grade}`, 10, 40);

    // Results table
    doc.autoTable({
      head: [['Subject', 'Score', 'Grade', 'Comment']],
      body: examResult.results.map(result => [
        result.subject,
        result.score,
        result.grade,
        result.comment
      ]),
      startY: 50,
      styles: { fontSize: 10 },
      headStyles: { fillColor: [74, 144, 226], textColor: 255 },
      alternateRowStyles: { fillColor: [240, 248, 255] },
    });

    const finalY = doc.lastAutoTable.finalY || 50;

    // Overall performance
    doc.setFontSize(14);
    doc.setTextColor('#4A90E2');
    doc.text('Overall Performance', 14, finalY + 20);
    addLine(finalY + 23, '#4A90E2');

    doc.setTextColor('#000000');
    doc.setFontSize(12);
    doc.text(`Average Score: ${examResult.average_score.toFixed(2)}`, 14, finalY + 35);
    doc.text(`Overall Grade: ${examResult.overall_grade}`, 14, finalY + 45);
    
    doc.text('Overall Comment:', 14, finalY + 60);
    doc.setFont('helvetica', 'italic');
    doc.text(examResult.overall_comment, 14, finalY + 70, { maxWidth: pageWidth - 28 });

    // Footer
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8);
    doc.text(`${schoolInfo.value.name} - Academic Report - Page ${index + 2} of ${examResults.value.length + 1}`, pageWidth / 2, pageHeight - 10, { align: 'center' });
  });
  
  // Principal's remark
  if (schoolInfo.value.principal_remark) {
    doc.addPage();
    doc.setFontSize(18);
    doc.setTextColor('#4A90E2');
    doc.text("Principal's Remark", 20, 20);
    addLine(25, '#4A90E2');
    doc.setFontSize(12);
    doc.setTextColor('#000000');
    doc.text(schoolInfo.value.principal_remark, 20, 40, { maxWidth: pageWidth - 40 });
  }

  const fileName = learnerInfo.value.name 
    ? `${learnerInfo.value.name.replace(/\s+/g, '_')}_academic_report.pdf`
    : 'academic_report.pdf';

  doc.save(fileName);
};

defineExpose({ fetchGrades })
</script>

<style scoped>
/* Add your styles here */
</style>

