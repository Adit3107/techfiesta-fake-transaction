import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    Brush,
} from 'recharts'

interface TimeSeriesData {
    timestamp: string
    total_amount: number
    anomaly_count: number
    [key: string]: any
}

interface TimeSeriesChartProps {
    timeSeries: TimeSeriesData[]
}

export default function TimeSeriesChart({ timeSeries }: TimeSeriesChartProps) {
    if (!timeSeries || timeSeries.length === 0) {
        return null
    }

    return (
        <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
                Transaction Volume Over Time
            </h3>
            <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                        data={timeSeries}
                        margin={{
                            top: 5,
                            right: 30,
                            left: 20,
                            bottom: 5,
                        }}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="timestamp" />
                        <YAxis yAxisId="left" />
                        <YAxis yAxisId="right" orientation="right" />
                        <Tooltip />
                        <Legend />
                        <Brush dataKey="timestamp" height={30} stroke="#8884d8" />
                        <Line
                            yAxisId="left"
                            type="monotone"
                            dataKey="total_amount"
                            stroke="#3b82f6"
                            activeDot={{ r: 8 }}
                            name="Transaction Amount"
                        />
                        <Line
                            yAxisId="right"
                            type="monotone"
                            dataKey="anomaly_count"
                            stroke="#ef4444"
                            name="Anomalies"
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}
