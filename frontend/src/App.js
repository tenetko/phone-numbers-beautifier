import { Button, Layout, message, Space, Upload } from "antd";
import axios from "axios";
import { useState } from "react";
import { UploadOutlined } from "@ant-design/icons";
import "antd/dist/reset.css";

const { Content } = Layout;

const buttonStyle = {
  textAlign: "center",
  color: "#000",
  height: 64,
  width: 300,
  paddingInline: 50,
  lineHeight: "57px",
  backgroundColor: "#d1b3ff",
};

const submitButtonStyle = {
  textAlign: "center",
  color: "#fff",
  height: 64,
  width: 300,
  paddingInline: 50,
  lineHeight: "57px",
  backgroundColor: "#39008f",
};

export default function App() {
  const [fileList, setFileList] = useState([]);
  const [uploading, setUploading] = useState(false);

  const handleUpload = () => {
    const formData = new FormData();

    fileList.forEach((file) => {
      formData.append("files", file);
    });

    setUploading(true);

    axios
      .post("http://localhost:8000/api/excel/handle/", formData, {})
      .then((res) => {
        setFileList([]);
        message.success("Файлы отправлены");
      })

      .catch(function (error) {
        message.error("Не получилось отправить файлы");
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
      <Content>
        <br />
        <br />
        <br />
        <br />
        <Space
          size="large"
          direction="vertical"
          align="center"
          style={{ width: "100%" }}
        >
          <Upload {...props}>
            <Button style={buttonStyle} icon={<UploadOutlined />}>
              Выгрузка из базы
            </Button>
            <br />
            <br />
            <Button style={buttonStyle} icon={<UploadOutlined />}>
              Исходник
            </Button>
            <br />
            <br />
            <Button style={buttonStyle} icon={<UploadOutlined />}>
              Файл с квотами
            </Button>
            <br />
            <br />
            <Button style={buttonStyle} icon={<UploadOutlined />}>
              Файл Alive
            </Button>
          </Upload>
          <br />
          <br />
          <Button
            type="primary"
            onClick={handleUpload}
            disabled={fileList.length === 0}
            loading={uploading}
            style={submitButtonStyle}
            block
          >
            {uploading ? "Загружаем..." : "Загрузить"}
          </Button>
        </Space>
      </Content>
    </Layout>
  );
}
