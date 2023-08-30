import './App.css'
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Settings } from './screens/settings/Settings';
import { Library } from './screens/libraries/Library';
import { TopBar } from './components/TopBar/TopBar';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Words } from './screens/words/Words';

const queryClient = new QueryClient()

function App() {
    return (
        <>
            <QueryClientProvider client={queryClient}>
                <BrowserRouter basename="/">
                    <TopBar />
                    <Routes>
                        <Route path="/settings" Component={Settings} />
                        <Route path="/libraries" Component={Library} />
                        <Route path="/words" Component={Words} />
                        {/* default route */}
                        <Route path="/" Component={Library} />
                    </Routes>
                    <ToastContainer />
                </BrowserRouter>
            </QueryClientProvider>
        </>
    )
}

export default App
