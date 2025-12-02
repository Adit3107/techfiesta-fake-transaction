interface SummaryData {
    total_transactions: number
    anomaly_count: number
    anomaly_percentage: number
    total_volume: number
    [key: string]: any
}

interface SummaryCardProps {
    summary: SummaryData
}

export default function SummaryCard({ summary }: SummaryCardProps) {
    const stats = [
        {
            name: 'Total Transactions',
            value: summary.total_transactions.toLocaleString(),
            color: 'bg-blue-500',
        },
        {
            name: 'Anomalies Detected',
            value: summary.anomaly_count.toLocaleString(),
            color: 'bg-red-500',
        },
        {
            name: 'Anomaly Rate',
            value: `${summary.anomaly_percentage.toFixed(2)}%`,
            color: 'bg-yellow-500',
        },
        {
            name: 'Total Volume',
            value: `$${summary.total_volume.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
            color: 'bg-green-500',
        },
    ]

    return (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {stats.map((item) => (
                <div
                    key={item.name}
                    className="bg-white overflow-hidden shadow rounded-lg"
                >
                    <div className="p-5">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                <div className={`h-3 w-3 rounded-full ${item.color}`} />
                            </div>
                            <div className="ml-5 w-0 flex-1">
                                <dl>
                                    <dt className="text-sm font-medium text-gray-500 truncate">
                                        {item.name}
                                    </dt>
                                    <dd>
                                        <div className="text-lg font-medium text-gray-900">
                                            {item.value}
                                        </div>
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}
