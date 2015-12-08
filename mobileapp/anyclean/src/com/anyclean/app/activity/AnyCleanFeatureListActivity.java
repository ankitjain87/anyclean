package com.anyclean.app.activity;

import java.util.ArrayList;
import java.util.List;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ListView;

import com.anyclean.app.R;
import com.anyclean.app.adapter.Feature;
import com.anyclean.app.adapter.FeatureAdapter;

public class AnyCleanFeatureListActivity extends ActionBarActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		// getApplicationContext().startService(new Intent(this,
		// FirstHttpCallIntentServeice.class));
		setContentView(R.layout.activity_any_clean_featur_list);
	}

	@Override
	protected void onResume() {
		super.onResume();
		final ListView listview = (ListView) findViewById(R.id.linearLayout_listview1_features);
		final String[] features = getApplicationContext().getResources()
				.getStringArray(R.array.any_clean_feature);
		final List<Feature> featuresList = new ArrayList<Feature>();
		for (String feature : features) {
			featuresList.add(new Feature().setFeature(feature));
		}
		
		final FeatureAdapter featureAdapter = new FeatureAdapter(getApplicationContext(), -1, featuresList);
		
		listview.setAdapter(featureAdapter);
		
		listview.setOnItemClickListener(new OnItemClickListener() {

			@Override
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {
				switch(position){
				case 0://Request pickup case
					Log.d("AnyClean", "Request pickup case");
					break;
				case 1://Orders
					Log.d("AnyClean", "Orders");
					break;
				case 2://Rate List
					Log.d("AnyClean", "Rate List");
					break;
				case 3://Profile
					Log.d("AnyClean", "Profile");
					break;
				case 4://Settings
					Log.d("AnyClean", "Settings");
					break;
				case 5://Refer Friends
					Log.d("AnyClean", "Refer Friends");
					break;
				case 6://Feedback
					Log.d("AnyClean", "Feedback");
					break;
				default:
					Log.d("AnyClean", "Default");
				}
			}
		});
	}

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

}