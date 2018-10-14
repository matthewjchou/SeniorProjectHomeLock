package team03.clientproject;

//import android.content.Context;
//import android.net.ConnectivityManager;
//import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import java.net.InetAddress;

import java.net.Socket;


public class ClientJava extends AppCompatActivity {

    Button butt1;
    EditText edit1;

    public String code;
    public String response;
    public String repeat;

    private static final String TAG = "ClientJava";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_client);

        butt1 = findViewById(R.id.button);
        edit1 = findViewById(R.id.editText);

        butt1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                code = edit1.getText().toString(); // gets code from the password box
                edit1.setText("");
                new ConnectTask().execute();
            }
        });
    }

    public class ConnectTask extends AsyncTask<String, Void, String> {

        @Override
        protected void onPreExecute() {
            Log.d(TAG, "AsyncTask beginning using code: " + code);
            super.onPreExecute();
        }

        @Override
        protected String doInBackground(String... message) {
            try {
                Log.d(TAG, "Attempting to connect to socket");
                InetAddress serverAddress1 = InetAddress.getByName("172.20.10.6"); //change IP address based on LAN    |    172.20.10.6
                Socket s1 = new Socket(serverAddress1, 5007);
                Log.d(TAG, "Connected to socket on: (" + serverAddress1 + ", " + s1.getPort());

                BufferedOutputStream bos1 = new BufferedOutputStream(s1.getOutputStream());
                bos1.write(code.getBytes("UTF-8"));
                bos1.flush();

                BufferedReader serverResponse1 = new BufferedReader(new InputStreamReader(s1.getInputStream()));
                response = serverResponse1.readLine();
                Log.d(TAG, "Server response: " + response);

                s1.close();
                Log.d(TAG, "socket closed");

            } catch (IOException e) {
                System.exit(1);
            }
            return response;
        }

        @Override
        protected void onPostExecute(String response) {
            if(response.equals("Authorized")) {
                Toast.makeText(getApplicationContext(), "Authenticated", Toast.LENGTH_LONG).show();

                new BroadcastTask().execute();
            }
            else {
                Toast.makeText(getApplicationContext(), "Invalid", Toast.LENGTH_LONG).show();
            }
        }
    }

    public class BroadcastTask extends AsyncTask<String, Void, String> {

        @Override
        protected void onPreExecute(){
            super.onPreExecute();
        }
        @Override
        protected String doInBackground(String... strings) {
            try {
                InetAddress serverAddress2 = InetAddress.getByName("172.20.10.6"); //change IP address based on LAN    |    172.20.10.6
                Socket sock = new Socket(serverAddress2, 5008);

                BufferedOutputStream bos2 = new BufferedOutputStream(sock.getOutputStream());

                //BufferedReader serverResponse2 = new BufferedReader(new InputStreamReader(sock.getInputStream()));

                repeat = "here";

                while(true) {
                    bos2.write(repeat.getBytes("UTF-8"));
                    Thread.sleep(3000);
                    bos2.flush();
                    //response = serverResponse2.readLine();
                    //Log.d(TAG, "in broadcast, response: " + response);
                }
            } catch (IOException e) {
                System.exit(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return null;
        }
    }
}