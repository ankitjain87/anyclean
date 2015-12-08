package com.anyclean.app.intentservice;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import android.app.IntentService;
import android.content.Intent;

public class FirstHttpCallIntentServeice extends IntentService {

	public FirstHttpCallIntentServeice(String name) {
		super("FirstHttpCallIntentServeice");
		// TODO Auto-generated constructor stub
	}

	public FirstHttpCallIntentServeice(){
		super("FirstHttpCallIntentServeice");
	}
	@Override
	protected void onHandleIntent(Intent intent) {
		HttpClient client = new DefaultHttpClient();
		HttpPost post = new HttpPost("http://localhost:8012/registerUser/");

		List<NameValuePair> pairs = new ArrayList<NameValuePair>();
		pairs.add(new BasicNameValuePair("name", "testName"));
		pairs.add(new BasicNameValuePair("email_id", "testEmail@email.com"));
		pairs.add(new BasicNameValuePair("mobile", "0000000000"));
		try {
			post.setEntity(new UrlEncodedFormEntity(pairs));
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		HttpResponse response = null;
		try {
			response = client.execute(post);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		response.getParams();
	}

}
