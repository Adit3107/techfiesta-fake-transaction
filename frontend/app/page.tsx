'use client';

import { useState } from 'react'
import FileUpload from '../components/FileUpload'
import SummaryCard from '../components/SummaryCard'
import AnomaliesTable from '../components/AnomaliesTable'
import TimeSeriesChart from '../components/TimeSeriesChart'
import DownloadReportButton from '../components/DownloadReportButton'

export default function Home() {
    const [result, setResult] = useState<any>(null)
    const [error, setError] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState(false)

    const handleUpload = async (file: File) => {
        setIsLoading(true)
        setError(null)
        setResult(null)

        const formData = new FormData()
        formData.append('file', file)

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Failed to analyze file')
            }

            const data = await response.json()
            setResult(data)
        } catch (err: any) {
            setError(err.message)
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gray-100">
            <header className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900">
                                Fake Transaction Detector
                            </h1>
                            <p className="mt-1 text-sm text-gray-500">
                                Upload transaction data to detect anomalies and potential fraud
                            </p>
                        </div>
                        <div className="flex items-center space-x-2">
                            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                                API Online
                            </span>
                        </div>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
                <div className="space-y-8">
                    <section>
                        <h2 className="text-lg font-medium text-gray-900 mb-4">
                            Upload Transaction Data
                        </h2>
                        <FileUpload onUpload={handleUpload} isLoading={isLoading} />
                    </section>

                    {error && (
                        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                            <div className="flex">
                                <div className="flex-shrink-0">
                                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                    </svg>
                                </div>
                                <div className="ml-3">
                                    <h3 className="text-sm font-medium text-red-800">Error</h3>
                                    <p className="mt-1 text-sm text-red-700">{error}</p>
                                </div>
                            </div>
                        </div>
                    )}

                    {result && (
                        <div className="mt-8 space-y-8">
                            <SummaryCard summary={result.summary} />

                            <div className="w-full">
                                <TimeSeriesChart timeSeries={result.time_series} />
                            </div>

                            <AnomaliesTable anomalies={result.anomalies} />

                            <DownloadReportButton
                                summary={result.summary}
                                anomalies={result.anomalies}
                            />
                        </div>
                    )}

                    {!result && !error && !isLoading && (
                        <div className="bg-white rounded-lg shadow p-8 text-center">
                            <div className="text-gray-400 mb-4">
                                <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                            </div>
                            <h3 className="text-lg font-medium text-gray-900 mb-2">
                                No Data Yet
                            </h3>
                            <p className="text-gray-500">
                                Upload a CSV file to analyze transactions and detect anomalies
                            </p>
                        </div>
                    )}
                </div>
            </main>

            <footer className="bg-white border-t mt-auto">
                <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
                    <p className="text-center text-sm text-gray-500">
                        Fake Transaction Detector - TECHFIESTA 2025
                    </p>
                </div>
            </footer>
        </div>
    )
}
