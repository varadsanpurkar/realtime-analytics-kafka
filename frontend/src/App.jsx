import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, Users, DollarSign, MousePointer } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function AnalyticsDashboard() {
  const [overview, setOverview] = useState({ total_events: 0, total_users: 0, total_sessions: 0, total_revenue: 0 });
  const [eventsByType, setEventsByType] = useState([]);
  const [eventsByCountry, setEventsByCountry] = useState([]);
  const [eventsByDevice, setEventsByDevice] = useState([]);
  const [topPages, setTopPages] = useState([]);
  const [timeline, setTimeline] = useState([]);
  const [recentEvents, setRecentEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [overviewRes, typeRes, countryRes, deviceRes, pagesRes, timelineRes, eventsRes] = await Promise.all([
        fetch(`${API_BASE}/stats/overview`),
        fetch(`${API_BASE}/stats/events-by-type`),
        fetch(`${API_BASE}/stats/events-by-country`),
        fetch(`${API_BASE}/stats/events-by-device`),
        fetch(`${API_BASE}/stats/top-pages`),
        fetch(`${API_BASE}/stats/timeline`),
        fetch(`${API_BASE}/events/recent?limit=10`)
      ]);

      setOverview(await overviewRes.json());
      setEventsByType(await typeRes.json());
      setEventsByCountry(await countryRes.json());
      setEventsByDevice(await deviceRes.json());
      setTopPages(await pagesRes.json());
      setTimeline(await timelineRes.json());
      setRecentEvents(await eventsRes.json());
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Real-Time Analytics Dashboard</h1>
          <p className="text-gray-400">Powered by Apache Kafka</p>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <StatCard
            icon={<Activity className="w-8 h-8" />}
            title="Total Events"
            value={overview.total_events.toLocaleString()}
            color="bg-blue-500"
          />
          <StatCard
            icon={<Users className="w-8 h-8" />}
            title="Unique Users"
            value={overview.total_users.toLocaleString()}
            color="bg-green-500"
          />
          <StatCard
            icon={<MousePointer className="w-8 h-8" />}
            title="Sessions"
            value={overview.total_sessions.toLocaleString()}
            color="bg-purple-500"
          />
          <StatCard
            icon={<DollarSign className="w-8 h-8" />}
            title="Revenue"
            value={`$${overview.total_revenue.toLocaleString()}`}
            color="bg-yellow-500"
          />
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <ChartCard title="Events Over Time">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={timeline}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="hour" stroke="#9ca3af" fontSize={12} />
                <YAxis stroke="#9ca3af" />
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                <Line type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>

          <ChartCard title="Events by Type">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={eventsByType}
                  dataKey="count"
                  nameKey="event_type"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {eventsByType.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Charts Row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <ChartCard title="Top Pages">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topPages} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis type="number" stroke="#9ca3af" />
                <YAxis dataKey="page" type="category" width={80} stroke="#9ca3af" />
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                <Bar dataKey="views" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>

          <ChartCard title="Events by Country">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={eventsByCountry}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="country" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                <Bar dataKey="count" fill="#f59e0b" />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Recent Events */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Recent Events</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="text-left py-2 px-4">User</th>
                  <th className="text-left py-2 px-4">Event</th>
                  <th className="text-left py-2 px-4">Page</th>
                  <th className="text-left py-2 px-4">Country</th>
                  <th className="text-left py-2 px-4">Device</th>
                  <th className="text-left py-2 px-4">Time</th>
                </tr>
              </thead>
              <tbody>
                {recentEvents.map((event) => (
                  <tr key={event.id} className="border-b border-gray-700 hover:bg-gray-700">
                    <td className="py-2 px-4">{event.user_id}</td>
                    <td className="py-2 px-4">
                      <span className={`px-2 py-1 rounded text-xs ${
                        event.event_type === 'purchase' ? 'bg-green-600' :
                        event.event_type === 'click' ? 'bg-blue-600' : 'bg-gray-600'
                      }`}>
                        {event.event_type}
                      </span>
                    </td>
                    <td className="py-2 px-4">{event.page_url}</td>
                    <td className="py-2 px-4">{event.country}</td>
                    <td className="py-2 px-4">{event.device}</td>
                    <td className="py-2 px-4 text-sm text-gray-400">
                      {new Date(event.timestamp).toLocaleTimeString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, title, value, color }) {
  return (
    <div className="bg-gray-800 rounded-lg p-6 flex items-center space-x-4">
      <div className={`${color} p-3 rounded-lg`}>{icon}</div>
      <div>
        <p className="text-gray-400 text-sm">{title}</p>
        <p className="text-2xl font-bold">{value}</p>
      </div>
    </div>
  );
}

function ChartCard({ title, children }) {
  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-4">{title}</h2>
      {children}
    </div>
  );
}