package com.anyclean.app.activity;

import com.anyclean.app.R;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

@SuppressWarnings("deprecation")
public class MainActivity extends ActionBarActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		// getApplicationContext().startService(new Intent(this,
		// FirstHttpCallIntentServeice.class));
		setContentView(R.layout.activity_main);
	}

	@Override
	protected void onResume() {
		super.onResume();
		// this.startService(new
		// Intent("com.example.test2.FirstHttpCallIntentServeice"));
		Button loginButton = (Button) this
				.findViewById(R.id.linearLayout_button1_login);
		EditText userNameEditText = (EditText) this
				.findViewById(R.id.linearLayout_edittext1_username);
		EditText passwordEditText = (EditText) this
				.findViewById(R.id.linearLayout_edittext2_password);
		TextView signUpTextView = (TextView) this
				.findViewById(R.id.linearLayout_textview2_signup);
		TextView forgotPassword = (TextView) this
				.findViewById(R.id.linearLayout_textview3_forgot_password);
		
		loginButton.setOnClickListener(clickListener);
		signUpTextView.setOnClickListener(clickListener);
		forgotPassword.setOnClickListener(clickListener);
		
	}

	OnClickListener clickListener = new OnClickListener() {

		@Override
		public void onClick(final View v) {
			switch (v.getId()) {
			case R.id.linearLayout_button1_login:
				//perform validation and login.
				startActivity(new Intent(getApplicationContext(), AnyCleanFeatureListActivity.class));
				break;
			case R.id.linearLayout_textview1_anyCleanIn_heading:
				//do something
				break;
			case R.id.linearLayout_textview2_signup:
				startActivity(new Intent(getApplicationContext(), RegistrationActivity.class));
				break;
			case R.id.linearLayout_textview3_forgot_password:
				//Launch forgot password activity
				break;
			default:
				Log.d("", "");
			}
		}
	};

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}
	
	@Override
	protected void onActivityResult(int arg0, int arg1, Intent arg2) {
		// TODO Auto-generated method stub
		super.onActivityResult(arg0, arg1, arg2);
	}
}
