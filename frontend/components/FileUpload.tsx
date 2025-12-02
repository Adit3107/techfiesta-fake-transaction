import { useState, useRef } from 'react'

interface FileUploadProps {
    onUpload: (file: File) => void
    isLoading: boolean
}

export default function FileUpload({ onUpload, isLoading }: FileUploadProps) {
    const [dragActive, setDragActive] = useState(false)
    const inputRef = useRef<HTMLInputElement>(null)

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true)
        } else if (e.type === 'dragleave') {
            setDragActive(false)
        }
    }

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault()
        e.stopPropagation()
        setDragActive(false)
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            onUpload(e.dataTransfer.files[0])
        }
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault()
        if (e.target.files && e.target.files[0]) {
            onUpload(e.target.files[0])
        }
    }

    const onButtonClick = () => {
        inputRef.current?.click()
    }

    return (
        <div
            className={`relative p-8 border-2 border-dashed rounded-lg text-center ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white'
                }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
        >
            <input
                ref={inputRef}
                type="file"
                className="hidden"
                onChange={handleChange}
                accept=".csv"
            />

            <div className="space-y-4">
                <div className="flex justify-center">
                    <svg className="h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </div>

                <div className="text-sm text-gray-600">
                    <button
                        type="button"
                        className="font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:underline"
                        onClick={onButtonClick}
                        disabled={isLoading}
                    >
                        Upload a file
                    </button>
                    {' '}or drag and drop
                </div>

                <p className="text-xs text-gray-500">CSV up to 10MB</p>

                {isLoading && (
                    <div className="mt-4">
                        <div className="inline-flex items-center px-4 py-2 font-semibold leading-6 text-sm shadow rounded-md text-white bg-blue-500 transition ease-in-out duration-150 cursor-not-allowed">
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Processing...
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
