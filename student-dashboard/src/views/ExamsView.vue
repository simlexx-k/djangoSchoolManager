<template>
  <div class="exams p-6 bg-gray-100 min-h-screen">
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800">Exam Results</h1>
        <button @click="exportAllExamsToPDF" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition duration-300 ease-in-out flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
          </svg>
          Export All to PDF
        </button>
      </div>

      <div v-if="isLoading" class="space-y-4">
        <div v-for="i in 3" :key="i" class="bg-white rounded-xl shadow-md p-6 animate-pulse">
          <div class="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div class="h-6 bg-gray-200 rounded w-1/2 mb-2"></div>
          <div class="h-6 bg-gray-200 rounded w-5/6 mb-4"></div>
          <div class="flex justify-between items-center">
            <div class="h-10 bg-gray-200 rounded w-1/4"></div>
            <div class="h-10 bg-gray-200 rounded w-1/4"></div>
          </div>
        </div>
      </div>

      <div v-else-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg" role="alert">
        <p class="font-bold">Error</p>
        <p>{{ error }}</p>
      </div>

      <div v-else-if="exams.length === 0" class="text-center py-10">
        <p class="text-2xl text-gray-600">No exam results available at the moment.</p>
      </div>

      <div v-else class="space-y-8">
        <div v-for="exam in exams" :key="exam.exam_id" 
             class="bg-white rounded-xl shadow-lg overflow-hidden transition duration-300 ease-in-out hover:shadow-xl">
          <div class="p-6">
            <div @click="toggleExam(exam.exam_id)" class="flex justify-between items-center mb-4 cursor-pointer">
              <h2 class="text-3xl font-semibold text-gray-800">{{ exam.exam_type }}</h2>
              <div class="flex items-center">
                <span class="text-sm font-medium text-gray-600 mr-4">{{ formatDate(exam.date) }}</span>
                <svg :class="{'transform rotate-180': expandedExam === exam.exam_id}" class="w-6 h-6 text-indigo-600 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </div>
            </div>
            <p class="text-xl text-gray-700 mb-4">Term: {{ exam.term }}</p>
            
            <div v-show="expandedExam === exam.exam_id" class="mt-6">
              <div class="bg-gray-50 rounded-lg p-6 mb-6">
                <h3 class="text-2xl font-semibold text-gray-800 mb-4">Results Summary</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div class="bg-white rounded-lg p-4 shadow">
                    <p class="text-sm font-medium text-gray-500">Average Score</p>
                    <p :class="getScoreClass(exam.average_score)" class="text-3xl font-bold">
                      {{ formatScore(exam.average_score) }}
                    </p>
                  </div>
                  <div class="bg-white rounded-lg p-4 shadow">
                    <p class="text-sm font-medium text-gray-500">Overall Grade</p>
                    <p :class="getGradeClass(exam.overall_grade)" class="text-3xl font-bold">
                      {{ exam.overall_grade }}
                    </p>
                  </div>
                  <div class="bg-white rounded-lg p-4 shadow">
                    <p class="text-sm font-medium text-gray-500">Overall Comment</p>
                    <p class="text-lg text-gray-700">{{ exam.overall_comment }}</p>
                  </div>
                </div>
              </div>

              <div class="overflow-x-auto bg-white rounded-lg shadow">
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
                    <tr v-for="result in exam.results" :key="result.subject">
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ result.subject }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <span :class="getScoreClass(result.score)" class="font-semibold">
                          {{ formatScore(result.score) }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <span :class="getGradeClass(result.grade)" class="px-2 py-1 rounded-full text-xs font-medium">
                          {{ result.grade }}
                        </span>
                      </td>
                      <td class="px-6 py-4 text-sm text-gray-500">{{ result.teacher_comment || 'No comment' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="mt-6 flex space-x-4">
                <button @click="viewExamDetails(exam.exam_id)" 
                        class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg shadow transition duration-300 ease-in-out flex items-center">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                  </svg>
                  View Details
                </button>
                <button @click="exportSingleExamToPDF(exam)" 
                        class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg shadow transition duration-300 ease-in-out flex items-center">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                  </svg>
                  Export This Exam
                </button>
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
import studentApi from '@/api/student'
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
import schoolLogo from '@/assets/masabaLogo.png'  // Import the logo
import QRCode from 'qrcode'

pdfMake.vfs = pdfFonts.pdfMake.vfs;

const exams = ref([])
const isLoading = ref(true)
const error = ref(null)
const expandedExam = ref(null)
const schoolLogoDataUrl = ref('')
const qrCodeDataUrl = ref('')

const convertImageToDataURL = (imgUrl) => {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.crossOrigin = 'Anonymous'
    img.onload = () => {
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')
      canvas.height = img.naturalHeight
      canvas.width = img.naturalWidth
      ctx.drawImage(img, 0, 0)
      const dataUrl = canvas.toDataURL()
      resolve(dataUrl)
    }
    img.onerror = error => reject(error)
    img.src = imgUrl
  })
}

onMounted(async () => {
  try {
    schoolLogoDataUrl.value = await convertImageToDataURL(schoolLogo)
  } catch (error) {
    console.error('Failed to convert school logo to data URL:', error)
  }
})

const fetchExams = async () => {
  try {
    const response = await studentApi.getExams()
    exams.value = response.data
    // Expand the first exam by default
    if (exams.value.length > 0) {
      expandedExam.value = exams.value[0].exam_id
    }
  } catch (error) {
    console.error('Error fetching exams:', error)
    error.value = 'Failed to load exam results. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const toggleExam = (examId) => {
  if (expandedExam.value === examId) {
    expandedExam.value = null
  } else {
    expandedExam.value = examId
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

const formatScore = (score) => {
  return score !== null ? score.toFixed(2) : 'N/A'
}

const getScoreClass = (score) => {
  if (score === null) return 'text-gray-500'
  if (score >= 80) return 'text-green-600'
  if (score >= 65) return 'text-blue-600'
  if (score >= 50) return 'text-yellow-600'
  return 'text-red-600'
}

const getGradeClass = (grade) => {
  switch (grade) {
    case 'EE': return 'bg-green-100 text-green-800'
    case 'ME': return 'bg-blue-100 text-blue-800'
    case 'AE': return 'bg-yellow-100 text-yellow-800'
    case 'BE': return 'bg-red-100 text-red-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

const viewExamDetails = (examId) => {
  // Implement navigation to exam details page
  console.log(`Viewing details for exam ${examId}`)
}

const generateQRCode = async (data) => {
  try {
    return await QRCode.toDataURL(data)
  } catch (err) {
    console.error('Error generating QR code:', err)
    return null
  }
}

const createExamPDFContent = async (exam) => {
  const qrCodeData = `${exam.school_name} - ${exam.student_name} - ${exam.exam_type} - ${exam.date}`
  qrCodeDataUrl.value = await generateQRCode(qrCodeData)

  return {
    content: [
      {
        columns: [
          {
            image: schoolLogoDataUrl.value,
            width: 60,
            alignment: 'left'
          },
          {
            stack: [
              { 
                text: exam.school_name,
                style: 'schoolName',
                alignment: 'right'
              },
              {
                text: 'Exam Results Report',
                style: 'mainHeader',
                alignment: 'right'
              }
            ],
            width: '*'
          }
        ],
        margin: [0, 0, 0, 20]
      },
      {
        canvas: [{ type: 'line', x1: 0, y1: 5, x2: 595 - 2*40, y2: 5, lineWidth: 3, lineColor: '#1e3a8a' }]
      },
      {
        columns: [
          {
            width: '*',
            text: [
              { text: 'Student: ', style: 'label' },
              { text: `${exam.student_name}\n`, style: 'value' },
              { text: 'Class: ', style: 'label' },
              { text: exam.student_grade, style: 'value' }
            ]
          },
          {
            width: '*',
            text: [
              { text: 'Exam: ', style: 'label' },
              { text: `${exam.exam_type}\n`, style: 'value' },
              { text: 'Date: ', style: 'label' },
              { text: formatDate(exam.date), style: 'value' }
            ],
            alignment: 'right'
          }
        ],
        margin: [0, 20, 0, 20]
      },
      {
        table: {
          headerRows: 1,
          widths: ['*', 'auto', 'auto', '*'],
          body: [
            [
              { text: 'Subject', style: 'tableHeader' },
              { text: 'Score', style: 'tableHeader' },
              { text: 'Grade', style: 'tableHeader' },
              { text: 'Comment', style: 'tableHeader' }
            ],
            ...exam.results.map(result => [
              result.subject,
              { 
                text: formatScore(result.score), 
                alignment: 'center',
                ...getScoreStyle(result.score)
              },
              { 
                text: result.grade, 
                alignment: 'center',
                ...getGradeStyle(result.grade)
              },
              result.teacher_comment || 'No comment'
            ])
          ]
        },
        layout: {
          hLineWidth: (i, node) => (i === 0 || i === node.table.body.length) ? 2 : 1,
          vLineWidth: (i, node) => (i === 0 || i === node.table.widths.length) ? 2 : 1,
          hLineColor: (i, node) => (i === 0 || i === node.table.body.length) ? '#1e3a8a' : '#e2e8f0',
          vLineColor: (i, node) => (i === 0 || i === node.table.widths.length) ? '#1e3a8a' : '#e2e8f0',
          fillColor: (rowIndex, node, columnIndex) => {
            return (rowIndex % 2 === 0) ? '#f0f9ff' : null;
          },
          paddingLeft: (i) => 8,
          paddingRight: (i) => 8,
          paddingTop: (i) => 8,
          paddingBottom: (i) => 8
        }
      },
      {
        columns: [
          {
            width: 'auto',
            text: [
              { text: 'Average Score: ', style: 'label' },
              { text: formatScore(exam.average_score), ...getScoreStyle(exam.average_score) }
            ]
          },
          {
            width: 'auto',
            text: [
              { text: 'Overall Grade: ', style: 'label' },
              { text: exam.overall_grade, ...getGradeStyle(exam.overall_grade) }
            ]
          }
        ],
        margin: [0, 20, 0, 10]
      },
      {
        text: [
          { text: 'Overall Comment: ', style: 'label' },
          { text: exam.overall_comment, style: 'value' }
        ],
        margin: [0, 0, 0, 20]
      },
      {
        canvas: [{ type: 'line', x1: 0, y1: 5, x2: 595 - 2*40, y2: 5, lineWidth: 1, lineColor: '#1e3a8a' }]
      },
      {
        columns: [
          {
            width: '*',
            text: `This is an official document of ${exam.school_name}`,
            style: 'footer',
            alignment: 'left'
          },
          {
            width: 'auto',
            image: qrCodeDataUrl.value,
            fit: [50, 50],
            alignment: 'right'
          }
        ],
        margin: [0, 20, 0, 0]
      }
    ],
    styles: getPDFStyles(),
    defaultStyle: {
      font: 'Roboto'
    }
  };
}

const exportSingleExamToPDF = async (exam) => {
  const docDefinition = await createExamPDFContent(exam);
  pdfMake.createPdf(docDefinition).download(`${exam.exam_type}_results.pdf`);
}

const exportAllExamsToPDF = async () => {
  const docDefinition = {
    content: await Promise.all(exams.value.map(async (exam) => {
      const examContent = await createExamPDFContent(exam);
      return [
        ...examContent.content,
        { text: '', pageBreak: 'before' }
      ];
    })),
    styles: getPDFStyles(),
    defaultStyle: {
      font: 'Roboto'
    }
  };
  pdfMake.createPdf(docDefinition).download('all_exam_results.pdf');
}

const getScoreStyle = (score) => {
  if (score === null) return { color: '#718096' };
  if (score >= 80) return { color: '#059669', bold: true };
  if (score >= 65) return { color: '#2563eb', bold: true };
  if (score >= 50) return { color: '#d97706', bold: true };
  return { color: '#dc2626', bold: true };
}

const getGradeStyle = (grade) => {
  switch (grade) {
    case 'EE': return { color: '#059669', bold: true, fontSize: 10 }; // Exceeding Expectations
    case 'ME': return { color: '#2563eb', bold: true, fontSize: 10 }; // Meeting Expectations
    case 'AE': return { color: '#d97706', bold: true, fontSize: 10 }; // Approaching Expectations
    case 'BE': return { color: '#dc2626', bold: true, fontSize: 10 }; // Below Expectations
    default: return { color: '#718096', bold: true, fontSize: 10 };
  }
}

const getPDFStyles = () => {
  return {
    schoolName: {
      fontSize: 18,
      bold: true,
      color: '#1e3a8a',
      margin: [0, 0, 0, 5]
    },
    mainHeader: {
      fontSize: 14,
      bold: true,
      color: '#4a5568',
      margin: [0, 0, 0, 5]
    },
    header: {
      fontSize: 14,
      bold: true,
      color: '#1e3a8a',
      margin: [0, 10, 0, 5]
    },
    tableHeader: {
      bold: true,
      fontSize: 12,
      color: '#ffffff',
      fillColor: '#1e3a8a'
    },
    label: {
      bold: true,
      fontSize: 10,
      color: '#4b5563'
    },
    value: {
      fontSize: 10,
      color: '#1f2937'
    },
    footer: {
      fontSize: 8,
      italics: true,
      color: '#6b7280'
    }
  };
}

onMounted(fetchExams)

defineExpose({ fetchExams })
</script>









