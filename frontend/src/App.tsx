import { Outlet } from 'react-router';

import { AppNavigationBar } from './AppNavigationBar';

export default function App() {
  return (
    <>
      <AppNavigationBar />
      <Outlet />
    </>
  );
}