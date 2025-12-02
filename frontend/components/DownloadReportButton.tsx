import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

interface Anomaly {
    transaction_id: string
    user_id: string
    amount: number
    timestamp: string
    city: string
    risk_score: number
    reasons: string[]
}

interface SummaryData {
    total_transactions: number
    anomaly_count: number
    anomaly_percentage: number
    total_volume: number
    [key: string]: any
}

interface DownloadReportButtonProps {
    summary: SummaryData
    anomalies: Anomaly[]
}

export default function DownloadReportButton({ summary, anomalies }: DownloadReportButtonProps) {
    const generatePDF = () => {
        const doc = new jsPDF()

        // Title
        doc.setFontSize(20)
        doc.text('Fake Transaction Analysis Report', 14, 22)

        doc.setFontSize(11)
        doc.text(`Generated on: ${new Date().toLocaleString()}`, 14, 30)

        // Summary Section
        doc.setFontSize(16)
        doc.text('Summary Statistics', 14, 45)

        const summaryData = [
            ['Total Transactions', summary.total_transactions.toLocaleString()],
            ['Total Volume', `$${summary.total_volume.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`],
            ['Anomalies Detected', summary.anomaly_count.toLocaleString()],
            ['Anomaly Rate', `${summary.anomaly_percentage.toFixed(2)}%`],
        ]

        autoTable(doc, {
            startY: 50,
            head: [['Metric', 'Value']],
            body: summaryData,
            theme: 'striped',
            headStyles: { fillColor: [59, 130, 246] }, // Blue color
        })

        // Anomalies Section
        const finalY = (doc as any).lastAutoTable.finalY || 50
        doc.setFontSize(16)
        doc.text('Detected Anomalies', 14, finalY + 15)

        const anomaliesData = anomalies.map(a => [
            a.transaction_id,
            a.user_id,
            `$${a.amount.toLocaleString()}`,
            new Date(a.timestamp).toLocaleString(),
            a.city,
            a.risk_score.toFixed(1),
            a.reasons.join(', ')
        ])

        autoTable(doc, {
            startY: finalY + 20,
            head: [['Tx ID', 'User', 'Amount', 'Time', 'City', 'Risk', 'Reasons']],
            body: anomaliesData,
            theme: 'grid',
            headStyles: { fillColor: [239, 68, 68] }, // Red color
            styles: { fontSize: 8 },
            columnStyles: {
                6: { cellWidth: 50 } // Wider column for reasons
            }
        })

        doc.save('transaction_analysis_report.pdf')
    }

    return (
        <div className="mt-8 flex justify-center">
            <button
                onClick={generatePDF}
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
                <svg className="-ml-1 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Download Summary Report
            </button>
        </div>
    )
}
