import { Button, Layout, message, Space, Typography, Upload } from "antd";
import axios from "axios";
import { useState } from "react";
import { routes } from "../../models/router";
import { UploadOutlined } from "@ant-design/icons";
import "antd/dist/reset.css";

const { Content } = Layout;
const { Text, Title } = Typography;

const buttonStyle = {
  textAlign: "center",
  color: "#000",
  height: 64,
  width: 300,
  paddingInline: 50,
  lineHeight: "57px",
  backgroundColor: "#94ffc9",
  marginTop: 20,
  marginBottom: 20,
};

const submitButtonStyle = {
  textAlign: "center",
  color: "#fff",
  height: 64,
  width: 300,
  paddingInline: 50,
  lineHeight: "57px",
  backgroundColor: "#005228",
};

const errorMessageStyle = {
  textAlign: "center",
  color: "#f00",  
};

const Page = () => {
  const [fileList, setFileList] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleUpload = () => {
    const formData = new FormData();

    fileList.forEach((file) => {
      formData.append("files", file);
    });

    console.log(formData);

    setUploading(true);

    const url = process.env.NODE_ENV === 'production'
      ? '/api/reminders/handle/'
      : 'http://127.0.0.1:8000/api/reminders/handle/'
    
    axios
      .post(url, formData, {responseType: "blob"})

      .then((response) => {
        setFileList([]);
        message.success("Файлы отправлены");
        const disposition = response.headers['content-disposition'];
        var filename = disposition.split(/;(.+)/)[1].split(/=(.+)/)[1];
        if (filename.toLowerCase().startsWith("utf-8''"))
          filename = decodeURIComponent(filename.replace("utf-8''", ''));
        else
          filename = filename.replace(/['"]/g, '');
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
      })

      .catch((error) => {
        message.error("Не получилось отправить файлы");
        console.log(error)
        if (
          error.request.responseType === 'blob' &&
          error.response.data instanceof Blob &&
          error.response.data.type &&
          error.response.data.type.toLowerCase().indexOf('json') !== -1
        ) {
          new Promise((resolve, reject) => {
              let reader = new FileReader();
              reader.onload = () => {
                error.response.data = JSON.parse(reader.result);                
                resolve(Promise.reject(error));
              };
    
              reader.onerror = () => {
                reject(error);
              };
    
              reader.readAsText(error.response.data);
            })

            .catch(error => {
              setErrorMessage(error.response.data);
            })
          };
      })

      .finally((res) => {
        setUploading(false);
      });
  };

  const props = {
    onRemove: (file) => {
      const index = fileList.indexOf(file);
      const newFileList = fileList.slice();
      newFileList.splice(index, 1);
      setFileList(newFileList);
    },

    beforeUpload: (file) => {
      setFileList([...fileList, file]);

      return false;
    },
    fileList,
  };

  return (
    <Layout>
      <Title level={1} style={{marginTop: 50, marginBottom: 50, textAlign: "center"}}>Reminders: apply quotas</Title>
      <Content>
      <Space direction="horizontal" style={{width: '100%', justifyContent: 'center'}}>
        <Typography.Text >
        <p>Upload the following files in any order:</p>
          <Text code>report_common_statistic_202309281119_265fd58c4014806f.xlsx</Text>
          <br/>
          <Text code>Reminder_2023424_03458.xlsx</Text>          
        </Typography.Text>        
        </Space>        
        <Space
          size="large"
          direction="vertical"
          align="center"
          style={{ width: "100%" }}
        >
          <Upload {...props}>
            <Button style={buttonStyle} icon={<UploadOutlined />}>
              Upload files
            </Button>
          </Upload>
          <Button
            type="primary"
            onClick={handleUpload}
            disabled={fileList.length === 0}
            loading={uploading}
            style={submitButtonStyle}
            block
          >
            {uploading ? "Uploading..." : "Submit"}
          </Button>
          <Text code style={errorMessageStyle}>{errorMessage}</Text>
        </Space>
      </Content>
    </Layout>
  );
}

export const RemindersPage = { Page, route: routes.reminders };
