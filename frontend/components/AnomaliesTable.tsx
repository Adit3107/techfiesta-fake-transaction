import { useState } from 'react'

interface Anomaly {
    transaction_id: string
    user_id: string
    amount: number
    city: string
    risk_score: number
    reasons: string[]
    [key: string]: any
}

interface AnomaliesTableProps {
    anomalies: Anomaly[]
}

export default function AnomaliesTable({ anomalies }: AnomaliesTableProps) {
    const [sortBy, setSortBy] = useState<string>('risk_score')
    const [sortDesc, setSortDesc] = useState(true)

    if (!anomalies || anomalies.length === 0) {
        return (
            <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
                No anomalies detected
            </div>
        )
    }

    const sortedAnomalies = [...anomalies].sort((a, b) => {
        const aVal = a[sortBy]
        const bVal = b[sortBy]
        if (sortDesc) {
            return aVal > bVal ? -1 : 1
        }
        return aVal > bVal ? 1 : -1
    })

    const handleSort = (column: string) => {
        if (sortBy === column) {
            setSortDesc(!sortDesc)
        } else {
            setSortBy(column)
            setSortDesc(true)
        }
    }

    const getRiskColor = (score: number) => {
        if (score >= 90) return 'bg-red-100 text-red-800'
        if (score >= 80) return 'bg-orange-100 text-orange-800'
        return 'bg-yellow-100 text-yellow-800'
    }

    const SortIcon = ({ column }: { column: string }) => {
        if (sortBy !== column) return null
        return <span className="ml-1">{sortDesc ? '↓' : '↑'}</span>
    }

    return (
        <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">
                    Detected Anomalies ({anomalies.length})
                </h3>
            </div>
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th
                                onClick={() => handleSort('transaction_id')}
                                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                            >
                                Transaction ID <SortIcon column="transaction_id" />
                            </th>
                            <th
                                onClick={() => handleSort('user_id')}
                                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                            >
                                User <SortIcon column="user_id" />
                            </th>
                            <th
                                onClick={() => handleSort('amount')}
                                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                            >
                                Amount <SortIcon column="amount" />
                            </th>
                            <th
                                onClick={() => handleSort('city')}
                                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                            >
                                City <SortIcon column="city" />
                            </th>
                            <th
                                onClick={() => handleSort('risk_score')}
                                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                            >
                                Risk Score <SortIcon column="risk_score" />
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Reasons
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {sortedAnomalies.map((anomaly, index) => (
                            <tr key={anomaly.transaction_id || index} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                    {anomaly.transaction_id}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {anomaly.user_id}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                    ${anomaly.amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {anomaly.city}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span
                                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRiskColor(
                                            anomaly.risk_score
                                        )}`}
                                    >
                                        {anomaly.risk_score.toFixed(1)}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-sm text-gray-500">
                                    <ul className="list-disc list-inside">
                                        {anomaly.reasons.map((reason, i) => (
                                            <li key={i} className="truncate max-w-xs">
                                                {reason}
                                            </li>
                                        ))}
                                    </ul>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
