import { useUser } from '../UserContext';

const Dashboard = () => {
  const { user } = useUser();  // Get user from context

  if (!user) {
    return <p>Please log in to access the dashboard.</p>;
  }

  return (
    <div>
      <h1>Welcome, {user.name || user.email}!</h1>
      <p>Email: {user.email}</p>
      <p>Premium Status: {user.is_premium ? 'Premium' : 'Standard'}</p>
      {user.picture && <img src={user.picture} alt="Profile" />}
    </div>
  );
};

export default Dashboard;
