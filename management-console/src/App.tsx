import './App.css'
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Settings } from './screens/settings/Settings';
import { Library } from './screens/library/Library';
import { TopBar } from './components/TopBar/TopBar';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Words } from './screens/words/Words';
import { MuiThemeProvider } from './theme/theme';
import { AdvancedSettings } from './screens/AdvancedSettings/AdvancedSettings';
import { ChangeLog } from './screens/ChangeLog/ChangeLog';
import { CheckUpdates } from './screens/CheckUpdates/CheckUpdates';
import { Logs } from './screens/Logs/Logs';
import { StickVisualization } from './screens/StickVisualization/StickVisualization';

const queryClient = new QueryClient()

function App() {
  return (
    <MuiThemeProvider>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter basename="/">
          <TopBar />
          <div style={{
            padding: "0 1rem", paddingTop: "2rem", flexGrow: 1, height: "calc(100vh - 4rem)", boxSizing: "border-box", justifyContent: "center", display: "flex"
          }}>
            < Routes >
              <Route path="/settings" Component={Settings} />
              <Route path="/library" Component={Library} />
              <Route path="/words" Component={Words} />
              <Route path="/stick_visualization" Component={StickVisualization} />
              <Route path="/advanced_settings" Component={AdvancedSettings} />
              <Route path="/logs" Component={Logs} />
              <Route path="/change_log" Component={ChangeLog} />
              <Route path="/check_updates" Component={CheckUpdates} />
              {/* default route */}
              <Route path="/" Component={Library} />
            </Routes>
          </div>
          <ToastContainer />
        </BrowserRouter>
      </QueryClientProvider >
    </MuiThemeProvider >
  )
}

export default App
