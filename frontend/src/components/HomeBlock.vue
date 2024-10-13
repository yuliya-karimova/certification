<template>
  <div class="max-w-screen-xl w-full flex flex-col gap-20">
    <!-- главная -->
    <div
      class="flex flex-col sm:flex-row items-center gap-6 lg:gap-12 font-mont max-sm:text-center"
    >
      <div class="flex-1">
        <div class="text-lg sm:text-2xl lg:text-3xl uppercase">Автоматизация</div>
        <h1 class="font-bold text-4xl sm:text-5xl md:text-6xl uppercase">проверки требований</h1>
        <div class="text-xl lg:text-2xl">в сертифицируемом контуре</div>
      </div>
      <div>
        <img alt="home pic" class="w-full h-auto" src="/auto.png" />
      </div>
    </div>

    <!-- анализ -->
    <div class="flex flex-col gap-12">
      <div class="space-y-6">
        <div class="space-y-2">
          <h2 class="text-xl md:text-3xl text-primary-800 font-mont">
            Введите текст требования для проверки:
          </h2>
          <BaseTextarea
            v-model="requirement"
            placeholder="Текст требования"
            class="w-full text-left"
            name="description"
            rows="10"
          />
        </div>
        <div class="space-y-2">
          <h2 class="text-xl md:text-3xl text-primary-800 font-mont">Или загрузите файл:</h2>
          <FileInput @uploaded="onFileUpload" />
        </div>
      </div>
      <div class="mb-12">
        <BaseButton theme="primary" :disabled="!requirement" @click="checkUseCase">
          Проверить корректность
        </BaseButton>
      </div>

      <!-- временный блок -->
      <!-- <div class="flex gap-4 items-start flex-col">
        <BaseButton theme="primary" :disabled="!requirement" @click="checkUseCase">
          Проверить корректность
        </BaseButton>

        <BaseButton theme="primary" :disabled="!requirement" @click="checkObjects">
          Проверить наличие объектов, подлежащих сертифицированию
        </BaseButton>

        <BaseButton theme="primary" :disabled="!requirement" @click="checkRegulations">
          Проверить соответствие регламентам
        </BaseButton>
      </div> -->
      <!-- временный блок -->

      <!-- результаты -->
      <div class="flex flex-col gap-24">
        <div v-if="checkResult.useCase">
          <div class="text-3xl font-bold text-accent-500 mb-6">Проверка на корректность</div>
          <MarkdownBlock :content="checkResult.useCase" />
          <div class="mt-12">
            <BaseButton theme="primary" @click="checkObjects">
              Проверить наличие объектов, подлежащих сертифицированию
            </BaseButton>
          </div>
        </div>

        <div v-if="checkResult.objects">
          <div class="text-3xl font-bold text-accent-500">
            Наличие объектов, подлежащих сертифицированию
          </div>
          <MarkdownBlock :content="checkResult.objects" />
          <div class="mt-12">
            <BaseButton theme="primary" @click="checkRegulations">
              Проверить соответствие регламентам
            </BaseButton>
          </div>
        </div>

        <div v-if="checkResult.regulations">
          <div class="text-3xl font-bold text-accent-500">Соответствие регламентам</div>
          <MarkdownBlock :content="checkResult.regulations" />
        </div>

        <div v-if="excelUrl && docxUrl && pdfUrl && !isChecking">
          <div class="text-xl font-bold text-accent-500 mb-4">
            Также можно скачать результаты проверки в PDF и Docx:
          </div>
          <div class="flex items-center gap-2">
            <!-- Ссылка для скачивания DOCX -->
            <a :href="docxUrl" target="_blank" download>
              <BaseButton theme="primary"> Скачать DOCX </BaseButton>
            </a>
            <!-- Ссылка для скачивания PDF -->
            <a :href="pdfUrl" target="_blank" download>
              <BaseButton theme="primary"> Скачать PDF </BaseButton>
            </a>
            <!-- Ссылка для скачивания excel -->
            <a v-if="excelUrl" :href="excelUrl" target="_blank" download>
              <BaseButton theme="secondary"> Скачать отчет Excel </BaseButton>
            </a>
          </div>
        </div>

        <div v-if="isChecking" class="flex gap-6 items-center">
          <BaseSpinner />
          <div>{{ checkingText }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useCheckStore } from '@/stores/check'
import BaseSpinner from '@/components/base/BaseSpinner.vue'
import BaseTextarea from '@/components/base/BaseTextarea.vue'
import BaseButton from '@/components/base/button/BaseButton.vue'
import MarkdownBlock from '@/components/MarkdownBlock.vue'
import FileInput from '@/components/FileInput.vue'

const requirement = ref('')
const fileName = ref('')

const isChecking = ref<boolean>(false)
const checkingText = ref('')
const checkResult = reactive({
  useCase: '',
  objects: '',
  regulations: ''
})

const docxUrl = ref('')
const pdfUrl = ref('')
const excelUrl = ref('')

const clearReports = () => {
  checkResult.useCase = ''
  checkResult.objects = ''
  checkResult.regulations = ''

  docxUrl.value = ''
  pdfUrl.value = ''
  excelUrl.value = ''
}

const checkStore = useCheckStore()

const onFileUpload = (text: string, fileNameValue: string) => {
  clearReports()

  requirement.value = text
  fileName.value = fileNameValue
}

const checkUseCase = async () => {
  isChecking.value = true
  checkingText.value = 'Проверяем use case на корректность'

  if (!fileName.value) {
    fileName.value = checkStore.getUuid()
  }

  const response = await checkStore.checkUseCase(requirement.value, fileName.value)

  checkResult.useCase = response.full_text
  docxUrl.value = checkStore.getDownloadLink(response.docx_url)
  pdfUrl.value = checkStore.getDownloadLink(response.pdf_url)

  isChecking.value = false
}

const checkObjects = async () => {
  isChecking.value = true
  checkingText.value = 'Проверяем наличие объектов, подлежащих сертифицированию'

  const response = await checkStore.checkObjects(requirement.value, fileName.value)

  checkResult.objects = response.full_text
  docxUrl.value = checkStore.getDownloadLink(response.docx_url)
  pdfUrl.value = checkStore.getDownloadLink(response.pdf_url)

  isChecking.value = false
}

const checkRegulations = async () => {
  isChecking.value = true
  checkingText.value = 'Проверяем соответстврие регламентам'

  const response = await checkStore.checkRegulations(requirement.value, fileName.value)

  checkResult.regulations = response.full_text
  docxUrl.value = checkStore.getDownloadLink(response.docx_url)
  pdfUrl.value = checkStore.getDownloadLink(response.pdf_url)

  if (response.excel_url) {
    excelUrl.value = checkStore.getDownloadLink(response.excel_url)
  }

  isChecking.value = false

  fileName.value = ''
}
</script>
