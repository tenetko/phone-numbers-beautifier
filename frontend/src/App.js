import { Layout, Typography } from "antd";

import { TZBPage } from "./pages/tzb";
import { RemindersPage } from "./pages/reminders";
import { Sidebar } from "./components/sidebar";
import { Route, RouterProvider } from "atomic-router-react";
import { router } from "./models/router";

import "antd/dist/reset.css";

const footerStyle = {
  textAlign: 'center',
  color: '#fff',
  backgroundColor: '#7dbcea',
};

export default function App() {
  return(
    <RouterProvider router={router}>
    <Layout style={{minHeight: "100vh"}}>
      <Sidebar/>
      <Layout>
        <Layout.Content>          
          <Route route={TZBPage.route} view={TZBPage.Page} />
          <Route route={RemindersPage.route} view={RemindersPage.Page} />
        </Layout.Content>      
        <Layout.Footer style={footerStyle}>
          <Typography.Text style={{textAlign: "center"}}>
            ver. 1.0.5 (with better ignore tab, gender and age, quotas filter, error notifications, and reminders)
          </Typography.Text>        
        </Layout.Footer>
      </Layout>
    </Layout>
    </RouterProvider>
    
    
  )
}
