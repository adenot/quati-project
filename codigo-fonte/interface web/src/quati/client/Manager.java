package quati.client;


import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.core.client.GWT;
import com.google.gwt.json.client.JSONObject;
import com.google.gwt.json.client.JSONParser;
import com.google.gwt.user.client.Timer;
import com.google.gwt.user.client.ui.RootPanel;
import com.gwtext.client.core.Connection;
import com.gwtext.client.core.EventObject;
import com.gwtext.client.core.Ext;
import com.gwtext.client.core.ExtElement;
import com.gwtext.client.core.Position;
import com.gwtext.client.core.SortDir;
import com.gwtext.client.data.BooleanFieldDef;
import com.gwtext.client.data.DataProxy;
import com.gwtext.client.data.FieldDef;
import com.gwtext.client.data.FloatFieldDef;
import com.gwtext.client.data.IntegerFieldDef;
import com.gwtext.client.data.JsonReader;
import com.gwtext.client.data.Record;
import com.gwtext.client.data.RecordDef;
import com.gwtext.client.data.ScriptTagProxy;
import com.gwtext.client.data.SimpleStore;
import com.gwtext.client.data.Store;
import com.gwtext.client.data.StringFieldDef;
import com.gwtext.client.data.event.StoreListenerAdapter;
import com.gwtext.client.widgets.Button;
import com.gwtext.client.widgets.Component;
import com.gwtext.client.widgets.MessageBox;
import com.gwtext.client.widgets.MessageBoxConfig;
import com.gwtext.client.widgets.PagingToolbar;
import com.gwtext.client.widgets.Panel;
import com.gwtext.client.widgets.TabPanel;
import com.gwtext.client.widgets.Toolbar;
import com.gwtext.client.widgets.ToolbarButton;
import com.gwtext.client.widgets.event.ButtonListenerAdapter;
import com.gwtext.client.widgets.event.PanelListenerAdapter;
import com.gwtext.client.widgets.form.Checkbox;
import com.gwtext.client.widgets.form.ComboBox;
import com.gwtext.client.widgets.form.Form;
import com.gwtext.client.widgets.form.FormPanel;
import com.gwtext.client.widgets.form.Hidden;
import com.gwtext.client.widgets.form.TextField;
import com.gwtext.client.widgets.form.event.FormListenerAdapter;
import com.gwtext.client.widgets.grid.CellMetadata;
import com.gwtext.client.widgets.grid.ColumnConfig;
import com.gwtext.client.widgets.grid.ColumnModel;
import com.gwtext.client.widgets.grid.GridPanel;
import com.gwtext.client.widgets.grid.Renderer;
import com.gwtext.client.widgets.grid.RowSelectionModel;
import com.gwtext.client.widgets.grid.event.RowSelectionListenerAdapter;
import com.gwtext.client.widgets.layout.ColumnLayout;
import com.gwtext.client.widgets.layout.ColumnLayoutData;

/**
 * Interface management for logs, rules and objects from the Quati Project.
 * 
 * This class creates a dynamic webpage with all the tools need by the administrator to manage the Quati
 * 
 * @author adenot
 */
public class Manager implements EntryPoint {

	private static final String REQUEST_URL = "http://quati/py/request.py/";
	
	/* Store controller */
	private Store[] stores = new Store[10];
	private int storesLast = 0;
	private boolean[] storesOk = new boolean[10];
	private Timer checkStoresTimer;
	
	/* Tab Panels */
	private TabPanel tabPanel;
	
	/* Panels */
	private Panel logPanel;
	private Panel rulePanel;
	private Panel ruleListPanel;
	private Panel ruleFormPanel;
	private Panel objectPanel;
	private Panel objectFormPanel;
	
	/* Grid Panels */
	private GridPanel logGrid;
	private GridPanel ruleListGrid;
	private GridPanel objectListGrid; 
	
	/* Form Panels */
	private FormPanel ruleForm;
	private FormPanel objectForm;
	
	/* Stores */
	private Store ruleStore;
	private Store logStore;
	private Store ruleServiceStore;
	private Store objectStore;
	
	/* Timers */
	private Timer ruleSubmitTimer;
	private Timer objectSubmitTimer;
	
	/* Toolbar Button */
	private ToolbarButton ruleListGridRemoveToolbarButton;
	private ToolbarButton objectListGridRemoveToolbarButton;
	
	/**
	 * This is the entry point method.
	 */
	public void onModuleLoad() {
		
		initializeStores();
		
		/* Create main Tabs */
		createTabs();
		
		/* Log Tab */
		renderLogViewer();
		
		/* Rule Tab */
		renderRuleViewer();
		renderRuleForm();
		
		/* Object Tab */
		renderObjectViewer();
		renderObjectForm();
			
		/* Add panels to main Tab */
		addPanels();
		
		/* Check stores for errors */
		checkAllStores();
		
	}
	
	private void initializeStores() {
		logStore = createStore(
				new ScriptTagProxy(REQUEST_URL+"?action=getLogList"),
				new JsonReader("logs",new RecordDef(new FieldDef[]{  
		                 new FloatFieldDef("timestamp"),
		                 new StringFieldDef("source"),  
		                 new StringFieldDef("destination"),  
		                 new StringFieldDef("service"),  
		                 new StringFieldDef("parameters")  }))
		);		
		
		// Rule Store
		ruleStore = createStore(
				new ScriptTagProxy(REQUEST_URL+"?action=getRuleList"),
				new JsonReader("rules",
					new RecordDef(
							new FieldDef[] {
									new IntegerFieldDef("id"),
									new StringFieldDef("description"),
					                new StringFieldDef("source_object"),  
					                new IntegerFieldDef("source_port"),
					                new StringFieldDef("destination_ip"),
					                new IntegerFieldDef("destination_port"),
					                new StringFieldDef("service"),  
					                new StringFieldDef("parameters"),
					                new BooleanFieldDef("enabled"),
					                new BooleanFieldDef("alert")
								}
						)
				)
		);
		ruleStore.sort("id",SortDir.ASC);
		
		// Object Store
		objectStore = createStore(
				new ScriptTagProxy(REQUEST_URL+"?action=getObjectList"),
				new JsonReader("objects",
					new RecordDef(
							new FieldDef[] {
									new IntegerFieldDef("id"),
									new StringFieldDef("name"),
					                new StringFieldDef("value"),  
								}
						)
				)
		);
		objectStore.sort("id",SortDir.ASC);

	}
	
	private void createTabs() {
		tabPanel = new TabPanel() {
			{
				setTabPosition(Position.TOP);  
				setResizeTabs(true);  
				setMinTabWidth(115);  
				setTabWidth(135);  
				setActiveTab(0);  				
			}
		};


		logPanel = new Panel("Logs");
		logPanel.setWidth("100%");
		
		rulePanel = new Panel("Rules");
		rulePanel.setLayout(new ColumnLayout());

		objectPanel = new Panel("Objects");
		objectPanel.setLayout(new ColumnLayout());
	}
	
	private void renderLogViewer() {


		
		/* Convert time from timestamp to a formatted date/time */
		ColumnConfig logColTimestamp = new ColumnConfig("Date/Time", "timestamp", 115, false);
		logColTimestamp.setRenderer(new Renderer() {
			public String render(Object value, CellMetadata cellMetadata,
					Record record, int rowIndex, int colNum, Store store) {
				String unixString = value.toString();
				Float unixFloat = Float.valueOf(unixString);
				int unixInt = unixFloat.intValue();
				return Common.convertTime(String.valueOf(unixInt));
			}
		});
		
		final ColumnModel logColumnModel = new ColumnModel(new ColumnConfig[]{ 
			logColTimestamp,
			new ColumnConfig("Source", "source", 115, false),
			new ColumnConfig("Destination", "destination", 115, false),
			new ColumnConfig("Service", "service", 60, false),
			new ColumnConfig("Parameters", "parameters", 300, false)
		});
		
		
		logGrid = new GridPanel() {
			{
				setStore(logStore);
				setColumnModel(logColumnModel);
				setWidth("100%");
				setHeight(400);
				setFrame(false);
				stripeRows(false);
				setBorder(false);				
			}
		};

		
		PagingToolbar logPagingToolbar = new PagingToolbar(logStore) {
			{
				setPageSize(50);  
				setDisplayInfo(true);
				setDisplayMsg("Displaying logs {0} - {1} of {2}");  
				setEmptyMsg("No logs to display");  				
			}
		};
		
		logGrid.setBottomToolbar(logPagingToolbar);
		
		/* on Render, load the first 50 rows */
		logGrid.addListener(new PanelListenerAdapter() {  
			public void onRender(Component component) {
				logStore.load(0, 50);
				}
			});  
		
		
		logPanel.add(logGrid);
		

		
		
	}
	
	private void renderRuleViewer() {
		
		// Rule Panel 
		ruleListPanel = new Panel("List") {
			{
				setWidth(200);
				setBorder(false);	
			}
		};
		

		
		// Rule List Grid
		
		ColumnConfig ruleColDescription = new ColumnConfig("Description", "description", 176, false);
		ruleColDescription.setFixed(false);
		final ColumnModel ruleColumnModel = new ColumnModel(new ColumnConfig[]{
				ruleColDescription
			});
		
		ruleListGrid = new GridPanel() {
			{
				setStore(ruleStore);
				setColumnModel(ruleColumnModel);
				setWidth("100%");
				setHeight(400);
				setFrame(false);
				stripeRows(false);
				setBorder(true);
				setHideColumnHeader(true);
			}
		};


		
		Toolbar ruleListGridToolbar = new Toolbar();
		ruleListGridRemoveToolbarButton = new ToolbarButton("Delete");
		ruleListGridToolbar.addButton(ruleListGridRemoveToolbarButton);		
		ruleListGrid.setBottomToolbar(ruleListGridRemoveToolbarButton);
		
		ruleListPanel.add(ruleListGrid);

		rulePanel.add(ruleListPanel);
		
	}

	private void renderRuleForm() {
		

		// Form Rule --------------------------------
		
		ruleFormPanel = new Panel("Add/Edit Rule");
		ruleFormPanel.setWidth("100%");
		ruleFormPanel.setBorder(false);
		
		ruleForm = new FormPanel() {
			{
				setLabelWidth(90);
				setAutoWidth(true);
				setMargins(5, 5, 5, 5);
				setTitle("Rule Details");  
				setLabelAlign(Position.RIGHT);
				setAutoHeight(true);  
				setFrame(false);	
				setHeader(false);
				setBorder(false);
				setButtonAlign(Position.LEFT);
				setUrl(REQUEST_URL+"?action=setRule");
				setMethod(Connection.GET);
			}
		};
		
		// Description TextField
		TextField ruleDescriptionTextField = new TextField("Description","description",200) {
			{
				setAllowBlank(false);
				setMsgFx("slideRight");
				setInvalidText("This field cannot be null");
				setLabelSeparator("&nbsp;");
			}
		};
		ruleForm.add(ruleDescriptionTextField);
		

		// Source Object ComboBox
		ComboBox ruleSourceObjectComboBox = new ComboBox("Source","source_object",200) {
			{
				setStore(objectStore);
				setMode(ComboBox.LOCAL);
				setEmptyText("Choose a source...");
				setSelectOnFocus(true);
				setEditable(false);
				setDisplayField("name");
				setValueField("id");
				setTriggerAction(ComboBox.ALL);
				setAllowBlank(false);
				setValue("0");
				setLabelSeparator("&nbsp;");
			}
		};
		ruleForm.add(ruleSourceObjectComboBox);
		
		// Destination Port Text Field
		
		TextField ruleDestinationPortTextField = new TextField("Destination Port","destination_port",200) {
			{
				setAllowBlank(true);
				setRegex("^[0-9]*$");
				setMsgFx("slideRight");
				setLabelSeparator("&nbsp;");
			}
		};
		ruleForm.add(ruleDestinationPortTextField);
		
		// Destination IP Text Field
		
		TextField ruleDestinationIpTextField = new TextField("Destination Ip","destination_ip",200) {
			{
				setAllowBlank(true);
				setRegex("^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$");
				setInvalidText("This field must contain a valid ip address");
				setMsgFx("slideRight");
				setLabelSeparator("&nbsp;");
			}
		};
		ruleForm.add(ruleDestinationIpTextField);
		
		// Service Store
		
		ruleServiceStore = new SimpleStore(new String[]{"service_name","service"}, 
				new String[][]{
					new String[]{"HTTP","HTTP"},
					new String[]{"All Services","ALL"}
		}); 
		
		// Service ComboBox
		
		ComboBox ruleServiceComboBox = new ComboBox("Service","service",200) {
			{
				setStore(ruleServiceStore);
				setMode(ComboBox.LOCAL);
				setEmptyText("Choose a service...");
				setSelectOnFocus(true);
				setEditable(false);
				setDisplayField("service_name");
				setValueField("service");
				setTriggerAction(ComboBox.ALL);
				setAllowBlank(false);
				setValue("ALL");
				setLabelSeparator("&nbsp;");
			}
		};
		ruleForm.add(ruleServiceComboBox);

		// Parameters Text Field
		
		TextField ruleParametersTextField = new TextField("Parameters","parameters",200) {
			{
				setAllowBlank(true);
				setLabelSeparator("&nbsp;");
				setMsgFx("slideRight");
			}};
		ruleForm.add(ruleParametersTextField);
		
		// Alert Checkbox
		
		Checkbox ruleAlertCheck = new Checkbox("Alert","alert");
		ruleAlertCheck.setInputValue("1");
		ruleForm.add(ruleAlertCheck);

		// Enabled Checkbox
		
		Checkbox ruleEnabledCheck = new Checkbox("Enable","enabled");
		ruleEnabledCheck.setInputValue("1");
		ruleForm.add(ruleEnabledCheck);
		
		// Id Hidden
		
		Hidden ruleIdHidden = new Hidden("id","0");
		ruleForm.add(ruleIdHidden);

		// Delete Hidden
		
		final Hidden ruleDeleteHidden = new Hidden("delete","0");
		ruleForm.add(ruleDeleteHidden);
		
		/**
		 * Submit Timer
		 * keep submiting until a Form.ActionComplete/Failed is achieved
		 */
		ruleSubmitTimer = new Timer(){ 
			@Override
			public void run() {
				ruleForm.getForm().submit();
			}
		};
		
		/**
		 * Save Button
		 * submit the form,
		 * program the Submit Timer
		 * mark the screen with a "saving..."
		 */
		final Button ruleSaveButton = new Button("Add",new ButtonListenerAdapter() {
			@Override
			public void onClick(Button button, EventObject e) {
				super.onClick(button, e);
				
				if (ruleForm.getForm().isValid()==false) {
					ruleForm.getForm().submit();
					return;
				}
				ruleForm.getForm().submit();
				ruleSubmitTimer.scheduleRepeating(4000);
				final ExtElement rulePanelElement = Ext.get(rulePanel.getId());
				rulePanelElement.mask("Saving...");
			}
		});
		
		ruleForm.addButton(ruleSaveButton);

		/**
		 * Cancel Button
		 * resets the form
		 * sets the Save button caption to Add
		 */
		Button ruleCancelButton = new Button("Cancel",new ButtonListenerAdapter() {
			@Override
			public void onClick(Button button, EventObject e) {
				super.onClick(button, e);
				ruleForm.getForm().reset();
				ruleSaveButton.setText("Add");
			}
		});

		ruleForm.addButton(ruleCancelButton);
		
		/**
		 * RowSelection
		 * when selected, the Record in the ruleListGrid is loaded into the ruleForm
		 */
		final RowSelectionModel ruleSM = new RowSelectionModel(true);  
		ruleSM.addListener(new RowSelectionListenerAdapter() {  
			public void onRowSelect(RowSelectionModel sm, int rowIndex, Record record) {  
				if (record.getAsInteger("destination_port")==0) {
					record.set("destination_port", "");
				}
				
				ruleForm.getForm().loadRecord(record);  
				ruleSaveButton.setText("Save");
			}  
		});  
		ruleListGrid.setSelectionModel(ruleSM);  

		ruleForm.addFormListener(new FormListenerAdapter() {
			@Override
			/**
			 * onActionComplete
			 * shows a messagebox
			 * reload the rules in the grid
			 * cancel the submit Timer
			 * unmask the panel
			 */
			public void onActionComplete(Form form, int httpStatus,
					String responseText) {
				super.onActionComplete(form, httpStatus, responseText);
				final JSONObject obj;
				try {
					obj=JSONParser.parse(responseText).isObject();
				} catch (Exception e) {
					return;
				}
				MessageBox.show(new MessageBoxConfig() {
					{
						setTitle("Success!");
						setMsg(obj.get("message").isString().stringValue());
						setAnimEl(ruleSaveButton.getId());
						setButtons(MessageBox.OK);
						setIconCls(MessageBox.INFO);
					}
				});

				ruleStore.reload();
				checkStore(ruleStore);
				ruleSubmitTimer.cancel();
				
				final ExtElement rulePanelElement = Ext.get(rulePanel.getId());
				rulePanelElement.unmask();
				form.reset();
			}
			@Override
			/**
			 * onActionFailed
			 * shows a messagebox
			 * cancels the submit Timer
			 * unmack the panel
			 */
			public void onActionFailed(Form form, int httpStatus,
					String responseText) {
				super.onActionFailed(form, httpStatus, responseText);
				final JSONObject obj=JSONParser.parse(responseText).isObject();
				MessageBox.show(new MessageBoxConfig() {
					{
						setTitle("Ooops!");
						setMsg(obj.get("message").isString().stringValue());
						setAnimEl(ruleSaveButton.getId());
						setButtons(MessageBox.OK);
						setIconCls(MessageBox.ERROR);
					}
				});
				ruleSubmitTimer.cancel();
				
				final ExtElement rulePanelElement = Ext.get(rulePanel.getId());
				rulePanelElement.unmask();
				ruleDeleteHidden.setValue("0");
			}
		});

		ruleListGridRemoveToolbarButton.addListener(new ButtonListenerAdapter() {
			@Override
			public void onClick(Button button, EventObject e) {
				super.onClick(button, e);
				
				if (ruleListGrid.getSelectionModel().hasSelection()==false) {
					MessageBox.show(new MessageBoxConfig() {
						{
							setTitle("Ooops!");
							setMsg("You must select a row to delete");
							setAnimEl(ruleListGridRemoveToolbarButton.getId());
							setButtons(MessageBox.OK);
							setIconCls(MessageBox.ERROR);
						}
					});
					return;
				}
				
				ruleForm.getForm().loadRecord(ruleSM.getSelected());
				
				MessageBox.show(new MessageBoxConfig() {
					{
					setTitle("Confirm");
					setMsg("Are you sure you want to delete?");
					setButtons(MessageBox.YESNO);
					setIconCls(MessageBox.QUESTION);
					setAnimEl(ruleListGridRemoveToolbarButton.getId());
					setCallback(new MessageBox.PromptCallback() {  
							public void execute(String btnID, String text) {  
								if (btnID.equals("yes")) {
									ruleDeleteHidden.setValue("1");
									ruleSaveButton.fireEvent("click");
								}
							}
						});
					}
				}); 	
			}
		
		});
		
		ruleFormPanel.add(ruleForm);
		rulePanel.add(ruleFormPanel,new ColumnLayoutData(1));
		
	}
	
	private void renderObjectViewer() {
		

		// Object List Panel -------------------------------------
		Panel objectListPanel = new Panel("List") {
			{
				setWidth(200);
				setBorder(false);	
			}
		};
		
		
		// Object List Grid
		
		ColumnConfig objectColDescription = new ColumnConfig("Name", "name", 176, false);
		objectColDescription.setFixed(false);
		final ColumnModel objectColumnModel = new ColumnModel(new ColumnConfig[]{
				objectColDescription
			});
		
		objectListGrid = new GridPanel() {
			{
				setStore(objectStore);
				setColumnModel(objectColumnModel);
				setWidth("100%");
				setHeight(400);
				setFrame(false);
				stripeRows(false);
				setBorder(true);
				setHideColumnHeader(true);
			}
		};


		
		Toolbar objectListGridToolbar = new Toolbar();
		objectListGridRemoveToolbarButton = new ToolbarButton("Delete");
		objectListGridToolbar.addButton(objectListGridRemoveToolbarButton);		
		objectListGrid.setBottomToolbar(objectListGridRemoveToolbarButton);
		
		objectListPanel.add(objectListGrid);

		objectPanel.add(objectListPanel);
		
		
		
		
	}
	
	private void renderObjectForm() {

		// Form Object --------------------------------
		
		objectFormPanel = new Panel("Add/Edit Object");
		objectFormPanel.setWidth("100%");
		objectFormPanel.setBorder(false);
		
		objectForm = new FormPanel() {
			{
				setLabelWidth(90);
				setAutoWidth(true);
				setMargins(5, 5, 5, 5);
				setTitle("Object Details");  
				setLabelAlign(Position.RIGHT);
				setAutoHeight(true);  
				setFrame(false);	
				setHeader(false);
				setBorder(false);
				setButtonAlign(Position.LEFT);
				setUrl(REQUEST_URL+"?action=setObject");
				setMethod(Connection.GET);
			}
		};
		// Description TextField
		
		TextField objectNameTextField = new TextField("Name","name",200) {
			{
				setAllowBlank(false);
				setMsgFx("slideRight");
				setInvalidText("This field cannot be null");
				setLabelSeparator("&nbsp;");
			}
		};
		objectForm.add(objectNameTextField);
		
		// Destination Port Text Field
		
		TextField objectValueTextField = new TextField("Value IP","value",200) {
			{
				setAllowBlank(true);
				setRegex("^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$");
				setInvalidText("This field must contain a valid ip address");
				setMsgFx("slideRight");
				setLabelSeparator("&nbsp;");
			}
		};
		objectForm.add(objectValueTextField);
		

		// Id Hidden
		
		Hidden objectIdHidden = new Hidden("id","0");
		objectForm.add(objectIdHidden);

		// Delete Hidden
		
		final Hidden objectDeleteHidden = new Hidden("delete","0");
		objectForm.add(objectDeleteHidden);
		
		/**
		 * Submit Timer
		 * keep submiting until a Form.ActionComplete/Failed is achieved
		 */
		objectSubmitTimer = new Timer(){ 
			@Override
			public void run() {
				objectForm.getForm().submit();
			}
		};
		
		/**
		 * Save Button
		 * submit the form,
		 * program the Submit Timer
		 * mark the screen with a "saving..."
		 */
		final Button objectSaveButton = new Button("Add",new ButtonListenerAdapter() {
			@Override
			public void onClick(Button button, EventObject e) {
				super.onClick(button, e);
				
				if (objectForm.getForm().isValid()==false) {
					objectForm.getForm().submit();
					return;
				}
				objectForm.getForm().submit();
				objectSubmitTimer.scheduleRepeating(4000);
				final ExtElement objectPanelElement = Ext.get(objectPanel.getId());
				objectPanelElement.mask("Saving...");
			}
		});
		
		objectForm.addButton(objectSaveButton);

		/**
		 * Cancel Button
		 * resets the form
		 * sets the Save button caption to Add
		 */
		Button objectCancelButton = new Button("Cancel",new ButtonListenerAdapter() {
			@Override
			public void onClick(Button button, EventObject e) {
				super.onClick(button, e);
				objectForm.getForm().reset();
				objectSaveButton.setText("Add");
			}
		});

		objectForm.addButton(objectCancelButton);
		
		/**
		 * RowSelection
		 * when selected, the Record in the objectListGrid is loaded into the objectForm
		 */
		final RowSelectionModel objectSM = new RowSelectionModel(true);  
		objectSM.addListener(new RowSelectionListenerAdapter() {  
			public void onRowSelect(RowSelectionModel sm, int rowIndex, Record record) {  
				if (record.getAsInteger("destination_port")==0) {
					record.set("destination_port", "");
				}
				
				objectForm.getForm().loadRecord(record);  
				objectSaveButton.setText("Save");
			}  
		});  
		objectListGrid.setSelectionModel(objectSM);  

		objectForm.addFormListener(new FormListenerAdapter() {
			@Override
			/**
			 * onActionComplete
			 * shows a messagebox
			 * reload the objects in the grid
			 * cancel the submit Timer
			 * unmask the panel
			 */
			public void onActionComplete(Form form, int httpStatus,
					String responseText) {
				super.onActionComplete(form, httpStatus, responseText);
				final JSONObject obj;
				try {
					obj=JSONParser.parse(responseText).isObject();
				} catch (Exception e) {
					return;
				}
				MessageBox.show(new MessageBoxConfig() {
					{
						setTitle("Success!");
						setMsg(obj.get("message").isString().stringValue());
						setAnimEl(objectSaveButton.getId());
						setButtons(MessageBox.OK);
						setIconCls(MessageBox.INFO);
					}
				});

				objectStore.reload();
				checkStore(objectStore);
				objectSubmitTimer.cancel();
				
				final ExtElement objectPanelElement = Ext.get(objectPanel.getId());
				objectPanelElement.unmask();
				form.reset();
			}
			@Override
			/**
			 * onActionFailed
			 * shows a messagebox
			 * cancels the submit Timer
			 * unmack the panel
			 */
			public void onActionFailed(Form form, int httpStatus,
					String responseText) {
				super.onActionFailed(form, httpStatus, responseText);
				final JSONObject obj=JSONParser.parse(responseText).isObject();
				MessageBox.show(new MessageBoxConfig() {
					{
						setTitle("Ooops!");
						setMsg(obj.get("message").isString().stringValue());
						setAnimEl(objectSaveButton.getId());
						setButtons(MessageBox.OK);
						setIconCls(MessageBox.ERROR);
					}
				});
				objectSubmitTimer.cancel();
				
				final ExtElement objectPanelElement = Ext.get(objectPanel.getId());
				objectPanelElement.unmask();
				objectDeleteHidden.setValue("0");
			}
		});

		objectListGridRemoveToolbarButton.addListener(new ButtonListenerAdapter() {
			@Override
			public void onClick(Button button, EventObject e) {
				super.onClick(button, e);
				
				if (objectListGrid.getSelectionModel().hasSelection()==false) {
					MessageBox.show(new MessageBoxConfig() {
						{
							setTitle("Ooops!");
							setMsg("You must select a row to delete");
							setAnimEl(objectListGridRemoveToolbarButton.getId());
							setButtons(MessageBox.OK);
							setIconCls(MessageBox.ERROR);
						}
					});
					return;
				}
				
				objectForm.getForm().loadRecord(objectSM.getSelected());
				
				MessageBox.show(new MessageBoxConfig() {
					{
					setTitle("Confirm");
					setMsg("Are you sure you want to delete?");
					setButtons(MessageBox.YESNO);
					setIconCls(MessageBox.QUESTION);
					setAnimEl(objectListGridRemoveToolbarButton.getId());
					setCallback(new MessageBox.PromptCallback() {  
							public void execute(String btnID, String text) {  
								if (btnID.equals("yes")) {
									objectDeleteHidden.setValue("1");
									objectSaveButton.fireEvent("click");
								}
							}
						});
					}
				}); 	
			}
		
		});
		
		objectFormPanel.add(objectForm);
		objectPanel.add(objectFormPanel,new ColumnLayoutData(1));
		
		
	}
	
	private void addPanels() {
		
		tabPanel.add(logPanel);	
		tabPanel.add(rulePanel);
		tabPanel.add(objectPanel);
		RootPanel.get("panelContent").add(tabPanel);
		
	}
	
	
	/**
	 * Automatize the creation of Stores
	 * also add to a global stores Array that will be used by checkAllStores
	 * @param dataProxy
	 * @param reader
	 * @return
	 * @see #checkAllStores()
	 */
	private Store createStore(DataProxy dataProxy, JsonReader reader) {
				
		reader.setTotalProperty("totalCount");  
		reader.setId("id");
		
		Store store = new Store(dataProxy,reader);
		
		store.addStoreListener(new StoreListenerAdapter() {
			@Override
			public void onLoad(Store store, Record[] records) {
				super.onLoad(store, records);
				for (int i=0;i<storesLast;i++) {
					if (stores[i]==store) {
						storesOk[i]=true;
						GWT.log("store ok: "+String.valueOf(i), null);
						System.out.println("store ok: "+String.valueOf(i));
					}
				}
			}
			
		});
				
		store.load();
		
		stores[storesLast] = store;
		storesLast++;
		
		return store;
	}
	
	/**
	 * Checks a store received
	 * resets the stores global array and add the received store
	 * @param store
	 */
	private void checkStore(Store store) {
		storesLast=1;
		stores[0]=store;
		
		checkStoresTimer = new Timer() {
			@Override
			public void run() {
				checkStoresTimed(checkStoresTimer);
			}
		};
		checkStoresTimer.scheduleRepeating(1000);
	}
	
	/**
	 * programs a timer to execute each 1000ms, checking if all stores are loaded successfully
	 * @see #checkStoresTimed(Timer)
	 */
	private void checkAllStores() {
		checkStoresTimer = new Timer() {
			@Override
			public void run() {
				checkStoresTimed(checkStoresTimer);
			}
		};
		checkStoresTimer.scheduleRepeating(1000 * storesLast);
	}
	
	/**
	 * verifies if the storesOk is given for each store in the global array
	 * if not, try to reload the store
	 * when all stores from the array are Ok, cancels the timer
	 * @param timer
	 */
	private void checkStoresTimed (Timer timer) {
		System.out.println("Checking Stores...");
		GWT.log("Checking Stores...",null);
		boolean canCancel = true;
		for (int i=0;i<storesLast;i++) {
			if (storesOk[i]!=true) {
				stores[i].reload();
				System.out.println("Reloading store "+String.valueOf(i));
				canCancel=false;
			}
		}
		if (canCancel==true) {
			timer.cancel();
		}
	}


}
