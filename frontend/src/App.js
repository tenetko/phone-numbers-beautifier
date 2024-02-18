import { Layout, Typography } from "antd";

<<<<<<< HEAD
import { TZBPage } from "./pages/tzb";
=======
import { TZBTemplatePage } from "./pages/tzbtemplate";
>>>>>>> templates
import { RemindersPage } from "./pages/reminders";
import { OSPage } from "./pages/os"
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
<<<<<<< HEAD
          <Route route={TZBPage.route} view={TZBPage.Page} />
=======
          <Route route={TZBTemplatePage.route} view={TZBTemplatePage.Page} />          
>>>>>>> templates
          <Route route={RemindersPage.route} view={RemindersPage.Page} />
          <Route route={OSPage.route} view={OSPage.Page} />
        </Layout.Content>      
        <Layout.Footer style={footerStyle}>
          <Typography.Text style={{textAlign: "center"}}>
            ver. 1.0.6: ignore tab, quotas filter, error notifications, reminders, and simple upload pages)
          </Typography.Text>     
        </Layout.Footer>
      </Layout>
    </Layout>
    </RouterProvider>
    
    
  )
}
